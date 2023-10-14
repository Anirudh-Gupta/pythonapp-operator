FROM python:3.6-slim-buster

## Adding telnet utility to aid in readiness probe - just to wait for db service to be up.
RUN apt-get update && apt-get install telnet

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["env", "FLASK_APP=app", "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]