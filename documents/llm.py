import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_archive.settings')
django.setup()

from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from django.db.models import Q
import re
from datetime import datetime
from .models import  Incoming, Outgoing, Internal, Decree

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LlmService():

    def __init__(self):
        logger.debug("Initializing LlmService...")
        self.model = AutoModelForTokenClassification.from_pretrained('./trained_model', trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained('./trained_model')
        logger.info("Model and tokenizer initialized.")

    def process_query(self, nlq):
        logger.debug(f"Processing query: {nlq}")

        # Tokenize and prepare input for the model
        inputs = self.tokenizer(nlq, return_tensors="pt")
        logger.debug(f"Tokenized inputs: {inputs}")

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits.argmax(dim=-1).squeeze().tolist()
            logger.debug(f"Model predictions: {predictions}")

        # Convert predictions to labels
        predicted_labels = [self.model.config.id2label[pred] for pred in predictions]
        logger.info(f"Predicted labels: {predicted_labels}")

        return predicted_labels
    
    def extract_filters_from_labels(self, nlq, predicted_labels):
        logger.debug(f"Extracting filters from labels for input: {nlq}")
        words = nlq.split()
        
        filters = {
            'dates': [],
            'years': [],
            'months': [],
            'days': [],
            'numbers': [],
            'keywords': [],
            'department': None,
            'affiliate': None,
            'government': None,
            'minister': None,
            'model_choice': [],
        }

        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day

        for word, label in zip(words, predicted_labels):
            logger.debug(f"Processing word: {word}, label: {label}")
            if label == "B-DATE":
                filters['dates'].append(word)
            elif label in ["B-YEAR", "I-YEAR"]:
                filters['years'].append(word)
            elif label in ["B-MONTH", "I-MONTH"]:
                filters['months'].append(word)
            elif label in ["B-DAY", "I-DAY"]:
                filters['days'].append(word)
            elif label in ["B-NUM", "I-NUM"]:
                filters['numbers'].append(word)
            elif label in ["B-KEY", "I-KEY"]:
                filters['keywords'].append(word)
            elif label in ["B-MIN", "I-MIN"]:
                filters['minister'] = word
            elif label in ["B-AFFT", "I-AFFT"]:
                filters['affiliate'] = word
            elif label in ["B-GOV", "I-GOV"]:
                filters['government'] = word
            elif label in ["B-DEPT", "I-DEPT"]:
                filters['department'] = word
            elif label in ["B-INC", "I-INC", "B-OUT", "I-OUT", 
                        "B-INT", "I-INT", "B-DEC", "I-DEC"]:
                filters['model_choice'].append(word)

        logger.info(f"Extracted filters: {filters}")

        # Initialize start_date and end_date
        start_date = None
        end_date = None

        # Process date components into universal date format
        if filters['dates']:
            start_date = collate_dates(filters['dates'][0])  # Set the first date found as start_date
            end_date = collate_dates(filters['dates'][-1])  # Set the last date found as end_date

        if filters['years']:
            # If only years are provided, set start and end dates for the range
            start_year = min(filters['years'])
            end_year = max(filters['years'])
            start_date = f"{start_year}-01-01" if not start_date else start_date
            end_date = f"{end_year}-12-31"  # End date for the last year

        if filters['months']:
            if not start_date:
                start_date = f"{current_year}-{filters['months'][0]}-01"
            end_month = max(filters['months'])
            end_day = (31 if end_month in ['01', '03', '05', '07', '08', '10', '12'] else
                        30 if end_month in ['04', '06', '09', '11'] else 
                        29 if end_month == '02' and (current_year % 4 == 0) else 
                        28)
            end_date = f"{current_year}-{end_month}-{end_day}"

        if filters['days']:
            if not start_date:
                start_date = f"{current_year}-{current_month}-{filters['days'][0]}"
            end_date = f"{current_year}-{current_month}-{int(filters['days'][-1]) + 1}"  # Last day + 1 for end_date

        # Only set start_date and end_date if they have been populated
        if start_date:
            filters['start_date'] = start_date
        if end_date:
            filters['end_date'] = end_date

        return filters
    
    def fetch_documents(self, filters):
        logger.debug("Fetching documents with the following filters:")
        logger.debug(filters)

        q_objects = Q()

        # Apply filters based on extracted criteria
        if filters['start_date']:
            q_objects &= Q(date__gte=filters['start_date'])
            logger.debug(f"Added start date filter: {filters['start_date']}")

        if filters['end_date']:
            q_objects &= Q(date__lte=filters['end_date'])
            logger.debug(f"Added end date filter: {filters['end_date']}")

        if filters['keywords']:
            keyword_queries = Q()
            for keyword in filters['keywords']:
                keyword_queries |= Q(title__icontains=keyword) | Q(keywords__icontains=keyword)
            q_objects &= keyword_queries
            logger.debug(f"Added keywords filter: {filters['keywords']}")

        if filters['minister']:
            q_objects &= Q(minister__name=filters['minister'])
            logger.debug(f"Added minister filter: {filters['minister']}")

        if filters['affiliate']:
            q_objects &= Q(affiliate__name=filters['affiliate'])
            logger.debug(f"Added affiliate filter: {filters['affiliate']}")

        if filters['department']:
            q_objects &= Q(department__name=filters['department'])
            logger.debug(f"Added department filter: {filters['department']}")

        if filters['government']:
            q_objects &= Q(government__name=filters['government'])
            logger.debug(f"Added government filter: {filters['government']}")

        model_mapping = {
            "B-INC": Incoming,
            "B-OUT": Outgoing,
            "B-INT": Internal,
            "B-DEC": Decree,
        }

        documents = None
        model_class = None
        # Fetch documents based on model choice
        for label in filters['model_choice']:
            model_class = model_mapping.get(label)
            if model_class:
                if documents is None:
                    documents = model_class.objects.filter(q_objects)
                    logger.debug(f"Initial documents fetched for {label}.")
                else:
                    documents = documents | model_class.objects.filter(q_objects)
                    logger.debug(f"Documents combined for {label}.")

        return documents

def collate_dates(date_str):
    logger.debug(f"Collating date: {date_str}")
    formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]  # Add more formats as needed
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue  # Try the next format
    logger.error(f"Date collating error: Invalid date format for {date_str}")
    return None
    
llm_service_instance = LlmService()