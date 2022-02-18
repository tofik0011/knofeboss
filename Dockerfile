FROM python:3.7
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir /src
WORKDIR /src
ADD . /src