FROM python:3.8.0b3-alpine3.10

ENV APP_ADDR=0.0.0.0 \
    APP_PORT=8080 \
    APP_DEBUG=True

ADD . /app

WORKDIR /app/

RUN set -xue; \
        mkdir ~/.pip/; \
        echo "\
[global] \n\
index-url = https://mirrors.aliyun.com/pypi/simple/ \n\
[install] \n\
trusted-host=mirrors.aliyun.com \n\
" > ~/.pip/pip.conf; \
        pip install -r requirements.txt;

EXPOSE 8080

CMD ["python", "webhook.py"]
