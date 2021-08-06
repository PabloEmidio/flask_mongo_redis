FROM python:3.9

RUN mkdir -p /banks/api

COPY requirements.txt /banks/api
WORKDIR /banks/api

RUN apt-get update
RUN pip3 install -r requirements.txt

EXPOSE 8088

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8088"]
CMD ["banks.app:create_app()"]