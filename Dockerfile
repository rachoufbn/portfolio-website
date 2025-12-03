FROM python:3.14-slim

# Install pip requirements
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

# During development this will be overwritten by a volume mount
COPY ./src/ .

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]