# flask_mongo_redis

## A basic CRUD application built in flask using redis and mongo as databases

# How to test now
## Make the following steps to debug this application inside a [docker container](https://docs.docker.com/get-started/)
  ``` 

  [example@example]$ git clone https://github.com/PabloEmidio/flask_mongo_redis.git

  [example@example]$ cd flask_mongo_redis

  [example@example flask_mongo_redis]$ docker-compose build

  [example@example flask_mongo_redis]$ docker-compose up -d

  [example@example flask_mongo_redis]$ URL="http://127.0.0.1:8088/"; xdg-open $URL || sensible-browser $URL || x-www-browser $URL || gnome-open $URL

  ```

## ps: import postman_collection inside your postman application to test the routes

