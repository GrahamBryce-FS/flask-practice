FROM ubuntu:20.04
RUN apt update && \
    apt install --no-install-recommends -y \
    python3.8 python3-pip python3.8-dev

WORKDIR . .

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3","app.py"]