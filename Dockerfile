FROM frolvlad/alpine-python3

MAINTAINER Junyong Suh "junyongsuh@gmail.com"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
