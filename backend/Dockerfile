
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

# RUN pip install build-essential libffi-dev
RUN pip3 install --upgrade pip setuptools wheel
RUN apk update && \
	apk add --no-cache mariadb-connector-c-dev && \
	apk add python3 python3-dev mariadb-dev build-base && \
	pip3 install mysqlclient && \
	apk del python3-dev mariadb-dev build-base
RUN apk add netcat-openbsd
# RUN apk add build-essential libssl-dev libffi-dev python-dev
# RUN apk add build-base libssl-dev libffi-dev python3-dev
# RUN apk add libffi-dev
RUN pip install -r /app/backend/requirements.txt
RUN pip install coverage
# RUN pip install channels
# RUN pip3 install uvicorn
# Copies from your local machine's current directory to the /app/backend folder in the Docker image
COPY ./entrypoint.sh /entrypoint.sh

COPY . .

# SECRET_KEY is only included here to avoid raising an error when generating static files.
# Be sure to add a real SECRET_KEY config variable in Heroku.
# RUN DJANGO_SETTINGS_MODULE=cycrent.settings.prod \
#     SECRET_KEY=TEST_SECRET_KEY \
#     python3 backend/manage.py collectstatic --noinput

# ENV PORT 8000
# EXPOSE 8000
# EXPOSE $PORT

# RUN ["ufw", "allow", "8000"]
RUN ["chmod", "+x", "/entrypoint.sh"]
# RUN ["chmod", "+x", "./manage.py"]
ENTRYPOINT ["/entrypoint.sh"]

# Create a user that can run your container
# RUN adduser -D user
# USER user

