# flask_mongo_redis

## A basic CRUD application built in flask using redis and mongo as databases

# How to test now
## Make the following steps to debug this application inside a [docker container](https://docs.docker.com/get-started/)
  ``` 

  [example@example]$ git clone https://github.com/PabloEmidio/flask_mongo_redis.git

  [example@example]$ cd flask_mongo_redis

  [example@example flask_mongo_redis]$ python -m venv .venv

  [example@example flask_mongo_redis]$ source .venv/bin/activate; pip install -r requirements.txt

  [example@example flask_mongo_redis]$ docker-compose up -d

  [example@example flask_mongo_redis]$ flask run

  ```

## ps: import postman_collection inside your postman application to test the routes

