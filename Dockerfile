FROM python:3.7.9

ADD server.py .

CMD ["python", "./server.py"]