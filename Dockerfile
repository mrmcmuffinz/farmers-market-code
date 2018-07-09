FROM python:3
WORKDIR /usr/src/farmers
COPY src/ ./
RUN python setup.py install