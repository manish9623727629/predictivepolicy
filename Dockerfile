FROM python

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt && \
    apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

WORKDIR /code/app

EXPOSE 80

CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:80", "app:app"]
