FROM python:slim

WORKDIR /tgbot 
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "gptbot.py"]