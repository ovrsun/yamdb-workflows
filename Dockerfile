FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r /app/api_yamdb/requirements.txt --no-cache-dir

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]
