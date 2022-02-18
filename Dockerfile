FROM python:3
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
RUN apt-get -y install vim
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /usr/src/app
#COPY requirements.txt ./
COPY ignore ./ignore
#COPY Model ./Model
#COPY Data ./Data
COPY *.py ./

RUN pip install --upgrade pip
#RUN pip install --upgrade setuptools
RUN pip install numpy
RUN pip install ccxt

#RUN pip install -r requirements.txt
CMD ["python","./Bot.py"]