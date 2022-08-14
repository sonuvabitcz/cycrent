FROM python:3.9-alpine
# Necessary, so Docker doesn't buffer the output and that you can see the output 
# of your application (e.g., Django logs) in real-time.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /requirements.txt
COPY ./scripts /scripts
COPY ./backend ./app

WORKDIR /app
EXPOSE 8000

ENV USER_NAME=app
ENV GROUP_NAME=app

# RUN addgroup -g $USER_ID $GROUP_NAME && \
#     adduser --shell /sbin/nologin --disabled-password \
#     --no-create-home --uid $USER_ID --ingroup $GROUP_NAME $USER_NAME
RUN adduser --disabled-password --no-create-home $USER_NAME

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
	apk add --update --no-cache mariadb-connector-c-dev && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base python3 python3-dev mariadb-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
	/py/bin/pip install coverage && \
    apk del .tmp-deps
# RUN pip3 install --upgrade pip
# RUN apk update && \
# 	apk add --no-cache mariadb-connector-c-dev && \
# 	apk add python3 python3-dev mariadb-dev build-base && \
# 	pip3 install mysqlclient && \
# 	apk add linux-headers && \
# 	pip install -r /requirements.txt && \
# 	apk del python3-dev mariadb-dev build-base
RUN mkdir -p /vol/web/static && \
	mkdir -p /vol/web/media && \
	chown $USER_NAME:$USER_NAME /vol -R && \
	chmod 755 /vol -R && \
	chown $USER_NAME:$USER_NAME /app -R && \
	chmod 755 /app -R && \
	chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER root
RUN id

CMD ["run.sh"]