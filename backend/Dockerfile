FROM python:3.9-alpine
# Necessary, so Docker doesn't buffer the output and that you can see the output 
# of your application (e.g., Django logs) in real-time.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/web
EXPOSE 8000

COPY ./requirements.txt /app/web/requirements.txt
COPY ./entrypoint.sh /entrypoint.sh
COPY . .

RUN pip3 install --upgrade pip
RUN apk update && \
	apk add --no-cache mariadb-connector-c-dev && \
	apk add python3 python3-dev mariadb-dev build-base && \
	pip3 install mysqlclient && \
	apk del python3-dev mariadb-dev build-base
RUN apk add netcat-openbsd && \
	pip install -r /app/web/requirements.txt && \
	pip install coverage
RUN mkdir -p /vol/web/static && \
	mkdir -p /vol/web/media
	# chown -R app:app /vol && \
	# chmod -R 755 /vol

# for deploying
# RUN apk add ufw build-essential libpq-dev libmysqlclient-dev python3.9-dev default-libmysqlclient-dev libpython3.9-dev
RUN pip3 install setuptools wheel && \
	apk add ufw libpq-dev

# USER app

# for deploying
# RUN ["ufw", "allow", "8000"]

RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]