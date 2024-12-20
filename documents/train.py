import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mail_archive.settings')
django.setup()


import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, Trainer, TrainingArguments, AutoModelForTokenClassification
from tqdm import tqdm  # For progress tracking
from transformers import default_data_collator

# CAMeL-Lab/bert-base-arabic-camelbert-da

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Custom collate_fn to pad sequences in the batch to the longest sequence in that batch
def collate_fn(batch):
    # Use the default collator to ensure other aspects (like labels) are handled correctly
    return default_data_collator(batch)


# Load your dataset
def load_dataset(file_path):
    logger.info(f"Loading dataset from {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    logger.info(f"Loaded dataset with {len(data['data'])} entries")
    return data

# Global variable for label mapping
label2id = {}

# Custom dataset class
class NERDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
            # Safely access encodings and labels
        if idx < len(self.encodings['input_ids']):
            item = {key: val[idx].clone().detach() for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item
        else:
            raise IndexError("Index out of bounds.")
        
    def __len__(self):
        return len(self.labels)
    
# Convert NER labels to numerical format
def encode_labels(labels, max_length, label2id):
    encoded_labels = []
    for label_seq in labels:
        # Convert the label sequence to its corresponding IDs
        encoded_seq = [label2id[label] for label in label_seq]

        # Pad the label sequence to the max_length
        padded_seq = encoded_seq + [label2id["O"]] * (max_length - len(encoded_seq))  # Assuming 'O' is the pad label
        
        # Ensure the padded sequence is truncated if it's longer than max_length
        padded_seq = padded_seq[:max_length]
        
        # Append the padded sequence to the list
        encoded_labels.append(padded_seq)
    
    return encoded_labels

def aggregate_labels(tokens, predicted_labels):
    aggregated_labels = []
    current_word = ""
    current_label = None

    for token, label in zip(tokens, predicted_labels):
        if label.startswith("B-"):  # Beginning of a new entity
            if current_label is not None:
                aggregated_labels.append((current_word, current_label))
            current_word = token.replace("##", "")  # Remove prefix
            current_label = label[2:]  # Store the entity type
        elif label.startswith("I-") and current_label is not None:
            current_word += token.replace("##", "")  # Append to the current word
        else:  # "O" label or no current entity
            if current_label is not None:
                aggregated_labels.append((current_word, current_label))
                current_label = None

    if current_label is not None:  # Append the last word
        aggregated_labels.append((current_word, current_label))

    return aggregated_labels

# Main function
def main():
    # Load dataset
    dataset = load_dataset('training_data.json')  # Change this to your JSON file path

    # Extract sentences and labels
    sentences = [entry['sentence'] for entry in dataset['data']]
    label_sequences = [entry['labels'] for entry in dataset['data']]

    logger.info(f"Extracted {len(sentences)} sentences and {len(label_sequences)} label sequences.")

    # Define label mapping
    unique_labels = set(label for seq in label_sequences for label in seq)
    label2id = {label: idx for idx, label in enumerate(unique_labels)}
    id2label = {idx: label for label, idx in label2id.items()}

    logger.info(f"Unique labels: {unique_labels}")

    # Tokenize the sentences
    tokenizer = AutoTokenizer.from_pretrained('google-bert/bert-base-uncased')


    # Encode labels
    encoded_labels = encode_labels(label_sequences, max_length=16, label2id=label2id)

    # Tokenize the training and test sentences
    train_encodings = tokenizer(sentences, truncation=True, padding='longest', add_special_tokens=True, return_tensors='pt', is_split_into_words=True, return_offsets_mapping=True)

    logger.info(f"Train Encodings: {train_encodings}")

    # Create datasets
    train_dataset = NERDataset(train_encodings, encoded_labels)

    logger.info(f"Training dataset size: {len(train_dataset)}")
    logger.info(f"Training Labels size: {len(encoded_labels)}")
    # Load pre-trained BERT model for token classification
    model = AutoModelForTokenClassification.from_pretrained(
        'google-bert/bert-base-uncased',
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id,
        trust_remote_code=True
    )

    # Define training arguments
    training_args = TrainingArguments(
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        fp16=True,  # Enable mixed precision
        warmup_steps=10,
        weight_decay=0.01,
        logging_steps=10,  # Add logging to track progress
        save_strategy="no",  # Save the model after each epoch
    )

    # Create Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
    )

    logger.info("Starting training...")
    logger.info(f"Train Dataset size: {len(train_dataset)}")
    logger.info(f"Batch size: {training_args.per_device_train_batch_size}")

    # Train the model
    trainer.train()

    # Save the model manually
    model.save_pretrained('./trained_model')
    tokenizer.save_pretrained('./trained_model')

    # Optionally, save the training arguments separately if needed
    with open('./trained_model/training_args.json', 'w') as f:
        json.dump(training_args.to_dict(), f)

    logger.info("Model training complete. commencing evaluation..")

    # Define test sentences
    test_sentences = [
        "رسايل صادره في شهر يونيو سنة 2010",
        "اعطيني البريد الوارد في سنة 2011",
        "مذكرة داخلية صادره من مكتب الشؤون القانونية",
        "قرار من الوزير محمد الحويج في سنة 2021",
        "قرارات سهيل ابوشيحه في من سنة 2010 الى 2020",
        "قرار رقمه 931 صادر في عام 2007",
        "رساله وارده من وزارة المالية بخصوص المرتبات",
        "كتاب صادر من مكتب العلامات بشان منظومة العلامات الجديده",
        "وارد برقم 7171 في سنة 2015",
        "مستند يحمل رقم 414 صادر من ادارة الشؤون الادرية والمالية بالوزارة"
    ]

    # Tokenize the test sentences
    test_encodings = tokenizer(test_sentences, truncation=True, padding='longest', add_special_tokens=True, return_tensors='pt', is_split_into_words=True, return_offsets_mapping=True)

    # Make predictions
    with torch.no_grad():
        model.eval()  # Set the model to evaluation mode
        outputs = model(**test_encodings)
        predictions = torch.argmax(outputs.logits, dim=2)  # Get the predicted class indices

    # Convert predictions to labels and log word-by-word
    for i, sentence in enumerate(test_sentences):
        # Tokenize the sentence to get the tokens used by the model
        tokens = tokenizer.tokenize(sentence)
        logger.info(f"Sentence: {tokens}")
        label_seq = [id2label[label_id.item()] for label_id in predictions[i]]

        # Aggregate labels for the tokens
        aggregated_labels = aggregate_labels(tokens, label_seq)

        # Log each aggregated word with its corresponding label
        logger.info(f"Sentence: {sentence}")
        for word, label in aggregated_labels:
            logger.info(f"Word: {word} | Predicted Label: {label}")

    logger.info("Test sentences processed and predictions made.")


if __name__ == '__main__':
    main()