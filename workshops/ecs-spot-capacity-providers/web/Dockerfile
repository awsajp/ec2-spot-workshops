FROM python:3.7.3-alpine3.9
COPY ./signals.py ./signals.py
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "signals.py"]

FROM python:3.8-slim

COPY / /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]
