FROM python:3.6

RUN apt-get update && apt-get install -y \
      gconf-service \
      libasound2 \
      libatk1.0-0 \
      libc6 \
      libcairo2 \
      libcups2 \
      libdbus-1-3 \
      libexpat1 \
      libfontconfig1 \
      libgcc1 \
      libgconf-2-4 \
      libgdk-pixbuf2.0-0 \
      libglib2.0-0 \
      libgtk-3-0 \
      libnspr4 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libstdc++6 \
      libx11-6 \
      libx11-xcb1 \
      libxcb1 \
      libxcomposite1 \
      libxcursor1 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxi6 \
      libxrandr2 \
      libxrender1 \
      libxss1 \
      libxtst6 \
      ca-certificates \
      fonts-liberation \
      libappindicator1 \
      libnss3 \
      lsb-release \
      xdg-utils \
      wget \
      cron

ADD ./requirements.txt /tmp/bot/requirements.txt
WORKDIR /tmp/bot
RUN pip install -r requirements.txt

COPY .env /tmp/.env

ADD . /tmp/bot

RUN echo 'SHELL=/bin/bash' >> /etc/crontab
RUN echo '* 2 * * 1-5 root source /tmp/.env;/usr/local/bin/python3 /tmp/bot/helthy_stand.py >>/tmp/bot.log 2>>/tmp/bot-err.log' >> /etc/crontab

CMD ["/usr/sbin/cron", "start", "&&", "tail", "-f", "/dev/null"]
