FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
# COPY poetry.lock .  # Uncomment if using Poetry

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

COPY . .

CMD ["python", "-m", "src.main"]