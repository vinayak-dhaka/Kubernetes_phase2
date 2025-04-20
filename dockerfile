
FROM python:3.12-slim

# Avoid interactive prompts during package installs
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system deps (if needed)
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade langchain langchain-openai
RUN pip install typing_extensions


# Copy source code
COPY . .

# Expose port and run app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
