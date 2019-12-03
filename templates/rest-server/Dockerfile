FROM alpine:latest

LABEL authors="Gabriele Baldoni, Luca Cominardi"


COPY ./libzenohc.so /usr/local/lib/libzenohc.so



RUN apk update && \
    apk add python3 git && \
    pip3 install flask flask_cors && \
    git clone http://github.com/atolab/zenoh-python && cd zenoh-python && git checkout 1ced877 && python3 setup.py install && cd .. &&\
    git clone http://github.com/atolab/yaks-python && cd yaks-python && git checkout 50c9fc7 && python3 setup.py install && cd .. && \
    git clone https://github.com/atolab/teleop_yaks && mv teleop_yaks/teleop_server.py /root/teleop_server.py && rm -r teleop_yaks



CMD python3 /root/teleop_server.py 172.16.123.30

