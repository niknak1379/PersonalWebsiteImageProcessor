Simple image processor to be deployed on lambda, changes format to avif and resizes

# Startup command

flask --app app.py run --debug
d

-- workflow test

if used or building an image for a flask webserver as was locally tested:
requirements.txt:
Flask==3.1.2
pillow==12.0.0
python-dotenv==1.2.0
boto3==1.41.2

dockerfile:

FROM python:3.15.0a2-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
