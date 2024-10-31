# Step 1: Use Python slim image as the base
FROM python:3.9-slim

# Step 2: Install Poetry
RUN pip install poetry

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /app/

# Step 5: Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Step 6: Copy the rest of the code
COPY . .

# Step 7: Define the command to run the application
CMD ["poetry", "run", "python", "main.py"]
