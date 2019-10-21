FROM python:3.7 as pyroles_bot
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
COPY . /src
RUN pip install -r /src/requirements.txt
WORKDIR /src
