# SWAMI KARUPPASWAMI THUNNAI

FROM python:3.6

RUN apt update
RUN apt install apache2 apache2-dev -y

RUN mkdir -p /var/www/candle_stick
COPY . /var/www/candle_stick
WORKDIR /var/www/candle_stick

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
RUN tar -xvf ta-lib-0.4.0-src.tar.gz
RUN cd ta-lib && ./configure --prefix=/usr
WORKDIR /var/www/candle_stick/ta-lib
RUN make
RUN make install
WORKDIR /var/www/candle_stick
RUN pip3 install -r requirements.txt
RUN pip3 install -t /usr/local/lib/python3.6/site-packages mod_wsgi
WORKDIR /var/www/candle_stick/docker_conf
RUN cat module.conf >> /etc/apache2/apache2.conf
RUN cat virtual_host.conf > /etc/apache2/sites-enabled/000-default.conf
CMD ["apachectl", "-D",  "FOREGROUND"]
