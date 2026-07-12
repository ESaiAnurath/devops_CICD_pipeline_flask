FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# gunicorn is a production-grade WSGI server (don't use Flask's dev server in prod)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
