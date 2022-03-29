# latest official alpine image
FROM python:latest

# add dependencies
RUN apt update
RUN apt install git

# add python modules
RUN python -m pip install --upgrade pip
RUN python -m pip install cffi
RUN python -m pip install youtube_dl
# RUN python -m pip install pymysql
RUN python3 -m pip install mysqlclient 
# RUN python3 -m pip install MySQL-python
# RUN python3 -m pip install cryptography
RUN python -m pip install pony

RUN git clone https://github.com/Pycord-Development/pycord.git

RUN python -m pip install -U ./pycord
WORKDIR /app
