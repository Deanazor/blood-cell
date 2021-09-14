FROM python:3.8

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["python", "app.py"]