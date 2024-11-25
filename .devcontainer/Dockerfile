FROM python:3.13-slim
RUN useradd -m vscode
WORKDIR /workspace
USER vscode
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . /workspace
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]