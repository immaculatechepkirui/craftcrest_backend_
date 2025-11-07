FROM python:3.9

RUN apt-get update && apt-get install -y \
    build-essential \
    libdbus-1-dev \
    libcups2-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
