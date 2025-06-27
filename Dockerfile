FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    uagents

CMD ["python", "agent.py"]
