FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Install dependencies using python -m pip (important)
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Verify spaCy is installed (debug-safe)
RUN python -c "import spacy; print(spacy.__version__)"

# Download spaCy model
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
