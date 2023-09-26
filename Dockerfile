FROM --platform=linux/amd64 python:3.9.17

WORKDIR /deal_finder

# Chrome installation
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

# Chrome Driver installation
ARG SCRIPT_FILE="get_chromedriver_download_url.py"

ARG CHROMEDRIVER_FILE_PATH="/tmp/chromedriver.zip"

COPY $SCRIPT_FILE /deal_finder

RUN wget -O $CHROMEDRIVER_FILE_PATH $(python3 /deal_finder/$SCRIPT_FILE linux64)

RUN unzip -j $CHROMEDRIVER_FILE_PATH "chromedriver*/chromedriver" -d /usr/local/bin/

RUN rm -rf /deal_finder/$SCRIPT_FILE $CHROMEDRIVER_FILE_PATH

# Project setup
COPY requirements.txt /deal_finder

RUN pip3 install -r requirements.txt

COPY ./deal_finder /deal_finder

CMD [ "python3", "-u", "main.py" ]
