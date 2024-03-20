FROM python:3.11

WORKDIR /app

RUN apt update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "yatube.asgi:application", "--host", "0.0.0.0", "--port", "8000"]