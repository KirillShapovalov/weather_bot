# pull official base image
FROM python:3.8.0-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add build-base
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN export LDFLAGS="-L/usr/local/opt/openssl/lib"
RUN pip install -r requirements.txt
# copy project
COPY . /usr/src/app/
EXPOSE 5000
# RUN ls -la app/
RUN curl --location --request POST 'https://api.telegram.org/bot{token}/setWebhook' --header 'Content-Type: application/json' --data-raw '{"url": "{url}"}'
RUN ./ngrok http 5000
ENTRYPOINT ["app/docker-entrypoint.sh"]