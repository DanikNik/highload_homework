FROM python:latest
ENV PY_NGINX_CONFIG_PATH="/etc/httpd.conf"
ENV PY_NGINX_HOST=0.0.0.0
ENV PY_NGINX_PORT=80

COPY ./httpd.conf /etc/httpd.conf
COPY ./http-test-suite /var/www/html
COPY ./src /py_nginx
WORKDIR /py_nginx
RUN pip install -r requirements.txt

EXPOSE 80
ENTRYPOINT python3 server.py
