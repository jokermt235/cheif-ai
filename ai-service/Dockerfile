FROM python:3.11

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0

WORKDIR /app

COPY ai-service/requirements.txt .
RUN pip install -r requirements.txt

COPY ai-service/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]