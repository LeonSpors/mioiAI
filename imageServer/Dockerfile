FROM python:3.7

COPY . /home/service
WORKDIR /home/service

RUN pip install -r requirements.txt

CMD [ "python", "./app.py" ]