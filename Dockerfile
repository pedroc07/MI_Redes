FROM python:3.7.9

ADD client.py .

CMD ["python", "./client.py"]