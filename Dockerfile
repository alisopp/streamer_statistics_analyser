FROM python:alpine
ARG db_port=27017
ARG db_host=127.0.0.1
ARG www_root="/"
ARG debug=True
ARG start_date="01.01.2019"
ARG credential="1"
ENV DB_PORT=${db_port}
ENV DB_HOST=${db_host}
ENV WWW_ROOT=${www_root}
ENV DEBUG=${debug}
ENV START_DATE=${start_date}
ENV TWITCH_CREDENTIALS=${credential}
ADD twitch_reader /twitch_reader

# Add crontab file in the cron directory
COPY crontab /etc/cron/crontab

# Give execution rights on the cron job
RUN chmod +x /etc/cron/crontab
RUN chmod +x /twitch_reader/entry.sh
# Apply cron job
RUN crontab /etc/cron/crontab

WORKDIR /twitch_reader
# Add python dependencies

RUN pip install requests
RUN pip install mongoengine
RUN pip install jinja2
#CMD ["crond", "-f"]
CMD [ "/bin/sh", "/twitch_reader/entry.sh"]