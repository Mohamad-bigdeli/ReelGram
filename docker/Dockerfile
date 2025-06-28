FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install uv
RUN apt-get update && \
    apt-get install -y curl unzip && \
    curl -L https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz | tar -xz && \
    mv uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/uv && \
    chmod +x /usr/local/bin/uv && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
    
RUN mkdir /app/

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# RUN uv pip compile requirements.txt --output-file requirements.lock.txt
# RUN uv pip sync --system requirements.lock.txt

COPY . .

