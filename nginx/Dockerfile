FROM nginx:latest

ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir /var/www/static

WORKDIR /var/www/static
ADD /static /var/www/static
RUN chown -R nginx:nginx /var/www/static