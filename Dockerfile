FROM python:3
MAINTAINER hien@wetbench.eu

WORKDIR /app
RUN pip install --no-cache-dir pandas
COPY . .
CMD bash
