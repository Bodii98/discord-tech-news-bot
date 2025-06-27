FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY bot.py .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash bot
USER bot

# Run the bot
CMD ["python", "bot.py"] 