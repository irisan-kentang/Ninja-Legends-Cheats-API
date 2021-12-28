FROM python:3.6

#update
RUN apt-get update

#install requirements
COPY ./requirements.txt /tmp/requirements.txt
WORKDIR /tmp
RUN pip3 install -r requirements.txt

#copy app
COPY . /api
WORKDIR /api

CMD ["gunicorn", "-w", "1", "-b", ":5000", "-t", "360", "--reload", "wsgi:app"]
