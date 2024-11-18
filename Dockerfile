# Use the official Windows Server Core image for Python 3.13
FROM python:3.13

# Set the working directory
WORKDIR D:\newP\mail\mail_archive

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]