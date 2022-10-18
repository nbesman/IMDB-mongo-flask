# Step 1 select default OS image
FROM alpine
# Step 2 Setting up environment
RUN apk add --no-cache python3-dev && apk add py3-pip
RUN pip3 install --upgrade pip
# Step 3 Configure a software
# Defining working directory
WORKDIR /IMDB-mongo-flask
# Installing dependencies.
COPY /requirements.txt /IMDB-mongo-flask
RUN pip3 install -r requirements.txt
# Copying project files.
COPY app.py /IMDB-mongo-flask
COPY MongoDBDAL.py /IMDB-mongo-flask
COPY TMDBDownLoader.py /IMDB-mongo-flask
COPY config.py /IMDB-mongo-flask
RUN mkdir -p /IMDB-mongo-flask/templates
RUN mkdir -p /IMDB-mongo-flask/temp_content
COPY ./templates/* /IMDB-mongo-flask/templates
# Exposing an internal port
EXPOSE 5001
# Step 4 set default commands
 # Default command
ENTRYPOINT [ "python3" ]
# These commands will be replaced if user provides any command by himself
CMD ["app.py"]