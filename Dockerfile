FROM python:3.11-alpine

RUN apk add --no-cache gcc bash

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000:8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]