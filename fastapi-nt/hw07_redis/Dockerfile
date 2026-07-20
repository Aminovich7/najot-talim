FROM python:3.13.5

WORKDIR /app

# Copy requirements first to leverage Docker's build cache
COPY requirements.txt .

# Install your dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project files
COPY . .

EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]