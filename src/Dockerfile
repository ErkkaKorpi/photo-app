FROM python:3.7-slim

ARG BUCKET
ARG KEY_ID
ARG SECRET_KEY
ARG DB_USER
ARG DB_PASS

WORKDIR /srv/photos-website

COPY requirements.txt /srv/photos-website

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install -r requirements.txt --src /urs/local/src

COPY . /srv/photos-website

RUN echo env=BUCKET=${BUCKET} >> /srv/photos-website/photos-website.ini
RUN echo env=KEY_ID=${KEY_ID} >> /srv/photos-website/photos-website.ini
RUN echo env=SECRET_KEY=${SECRET_KEY} >> /srv/photos-website/photos-website.ini
RUN echo env=DB_USER=${DB_USER} >> /srv/photos-website/photos-website.ini
RUN echo env=DB_PASS=${DB_PASS} >> /srv/photos-website/photos-website.ini

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
CMD ["./start.sh"]