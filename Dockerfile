FROM python:3
WORKDIR /app
RUN pip install --no-cache-dir pandas pdbio pyvcf
COPY . .
CMD bash
