FROM httpd:2.4.46-alpine


COPY ./mr_project /var/www/html/mr_project
ADD ./docker/httpd.conf /usr/local/apache2/conf/httpd.conf
ADD ./docker/entrypoint.sh /entrypoint.sh
ADD ./requirements.txt /tmp/requirements.txt
RUN chmod +x /entrypoint.sh

RUN apk update && apk add python3-dev==3.8.5-r0 py3-pip==20.1.1-r0 postgresql-dev==12.3-r2 \
    gcc==9.3.0-r2 musl-dev==1.1.24-r9 make==4.3-r0 expat-dev==2.2.9-r1 apache2-mod-wsgi==4.7.1-r0 \
    apr-dev==1.7.0-r0 apr-util-dev==1.6.1-r6 apache2-mod-wsgi==4.7.1-r0
RUN pip3 install -r /tmp/requirements.txt
RUN cp /usr/lib/apache2/mod_wsgi.so /usr/local/apache2/modules/

EXPOSE 80

CMD ["httpd-foreground"]
ENTRYPOINT ["/entrypoint.sh"]