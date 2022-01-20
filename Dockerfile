FROM --platform=linux/amd64 python:3.8 

RUN ["apt-get", "-y",  "update"]
RUN ["apt", "install", "-y", "wget", "gnupg", "curl"]

# Fetch google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN ["apt-get", "-y",  "update"]
RUN ["apt-get", "-y",  "upgrade"]
RUN ["apt-get", "install",  "-y", "google-chrome-stable"]

# Download chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN chmod +x /usr/local/bin/chromedriver

ENV DISPLAY=:99

COPY . /deliveroo-webscraping-team
WORKDIR /deliveroo-webscraping-team

ENV DB_HOST="del_db"
ENV DB_USER="del"
ENV DB_PASSWORD="ahj%ZF2*TIZk"
ENV DB_NAME="postgresdb"
ENV DB_PORT=5432

ENV SENTRY_DSN="https://d2744aa667304febbb8766ca55f650f8@o1086610.ingest.sentry.io/6098931"
ENV SENTRY_ENVIRONMENT="dev"

RUN ["pip3", "install", "-r", "requirements.txt"]
ENTRYPOINT [ "python3.8", "main.py" ]
