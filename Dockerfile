FROM python:3.12
WORKDIR /

COPY ta-lib ta-lib
WORKDIR /
WORKDIR /ta-lib
RUN ./configure --prefix=/usr --build=arm
RUN make
RUN make install

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "main_stream_usd.py"]