FROM python:3.6-slim

WORKDIR /app

RUN apt-get update -y && apt-get upgrade -y

RUN RUN apt-get install git -y

RUN git clone https://github.com/nodefluxio/vortex.git
RUN cd vortex && git checkout drop-enforce && pip install --ignore-installed --timeout=10000 ./src/runtime[onnxruntime]

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD ["python", "app.py"]