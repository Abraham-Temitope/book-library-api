FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Only copy the important parts
COPY ./app ./app
COPY ./requirements.txt . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# For development you can add --reload, but usually not in production images