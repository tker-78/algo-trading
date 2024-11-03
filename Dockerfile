# arm用
FROM python:3.12
WORKDIR /
COPY ta-lib-0.4.0-src.tar.gz ta-lib-0.4.0-src.tar.gz
RUN tar -xzf ta-lib-0.4.0-src.tar.gz
WORKDIR /ta-lib
RUN ./configure --prefix=/usr --build=arm
RUN make
RUN make install
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main_stream_usd.py"]

# amd用
FROM --platform=linux/amd64 python:3.12
WORKDIR /
COPY ta-lib-0.4.0-src.tar.gz ta-lib-0.4.0-src.tar.gz
RUN tar -xzf ta-lib-0.4.0-src.tar.gz
WORKDIR /ta-lib
RUN ./configure --prefix=/usr
RUN make
RUN make install
WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main_stream_usd.py"]