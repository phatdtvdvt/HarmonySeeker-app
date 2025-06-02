FROM python:3.13

WORKDIR /app

RUN pip install urllib3==1.26.18 \
    && pip install typing-extensions --upgrade \
    && pip install poetry

RUN poetry config virtualenvs.in-project true

# Copy pyproject.toml and poetry.lock first for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy source code
COPY . /app
