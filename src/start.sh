#!/usr/bin/env bash
service nginx start
sleep 10
uwsgi --ini photos-website.ini
