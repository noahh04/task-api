# Python Basis Image
FROM python:3.11

# Arbeitsverzeichnis im Container
WORKDIR /app

# Dependencies kopieren
COPY requirements.txt .

# Pakete installieren
RUN pip install --no-cache-dir -r requirements.txt

# Projekt kopieren
COPY . .

# Port öffnen
EXPOSE 8000

# Startbefehl
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
