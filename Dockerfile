FROM python:3.6

EXPOSE 8888

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 setup_keys.py

ENTRYPOINT ["python3", "app.py"]
