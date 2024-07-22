FROM python:3.11.9-slim-bookworm
WORKDIR /twnweather
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python", "./web/manage.py", "runserver", "0.0.0.0:8000", "--settings=web.settings" ]
