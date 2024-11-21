# Base Image
FROM seladb/ubuntu1804

# MAINTAINER
MAINTAINER Crawlergo Xray VulScan
# docker build -t xray .
# docker run -itd xray

ENV XRAY_VERSION "1.8.5"
ENV Crawlergo_VERSION "0.4.3"
ENV VERSION "Bate 20220719"
COPY crawlergo_linux_* /root/
COPY xray* /root/
COPY run.py /root/
COPY targets.txt /root/

# Running Command
RUN apt -y update && apt -y install vim chromium-browser
RUN chmod 777 /root/*
ENTRYPOINT cd /root/ && python3 run.py >> debug.log