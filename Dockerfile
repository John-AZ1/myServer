FROM python:3.7.2-slim

COPY mySimon /app
COPY myRoster /app
COPY desc.py /app
COPY index.py /app
COPY myServer.py /app
COPY requirements.txt /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080
WORKDIR /app
CMD ["python3", "-u", "index.py"]
