# The image you are going to inherit your Dockerfile from
FROM python:3.9-alpine
# Necessary, so Docker doesn't buffer the output and that you can see the output 
# of your application (e.g., Django logs) in real-time.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Make a directory in your Docker image, which you can use to store your source code
# RUN mkdir /django_recipe_api
# Set the /app/backend directory as the working directory
WORKDIR /app/backend

# Copy the requirements.txt file adjacent to the Dockerfile to your Docker image
COPY ./requirements.txt /app/backend/requirements.txt

RUN pip3 install --upgrade pip
RUN \
    apk update && \
	apk add --no-cache mariadb-connector-c-dev && \
	apk add python3 python3-dev mariadb-dev build-base && \
	pip3 install mysqlclient && \
	apk del python3-dev mariadb-dev build-base
RUN apk add netcat-openbsd
RUN pip install -r /app/backend/requirements.txt
# Copies from your local machine's current directory to the /app/backend folder in the Docker image
COPY ./entrypoint.sh /entrypoint.sh

COPY . .

RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT ["/entrypoint.sh"]

# Create a user that can run your container
# RUN adduser -D user
# USER user

