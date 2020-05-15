FROM python:3.7.3-alpine3.9
MAINTAINER jalawala@amazon.com
RUN wget https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-2.x.zip && unzip aws-xray-daemon-linux-2.x.zip && cp ./xray /usr/bin/xray
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]

EXPOSE 8000

CMD ["xray", "--log-file /var/log/xray-daemon.log"] &
CMD ["app.py"]