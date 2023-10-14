FROM python:3.7-slim
RUN mkdir /src
ADD k8s/ /src
ADD with_update.py /src
ADD requirements.txt /src
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /src/requirements.txt
CMD kopf run --standalone /src/with_update.py --verbose