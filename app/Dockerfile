FROM python:3.10.6

WORKDIR /app

COPY . .

RUN apt update && apt install curl -y

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r ./requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--reload"]