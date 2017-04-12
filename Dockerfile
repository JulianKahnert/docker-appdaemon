FROM python:3.4
MAINTAINER Julian Kahnert <mail@juliankahnert.de>
LABEL org.freenas.expose-ports-at-host="true" \
      org.freenas.port-mappings="5050:5050/tcp" \
      org.freenas.volumes="[ \
          { \
              \"name\": \"/conf\", \
              \"descr\": \"HADashboard config\" \
          } \
      ]"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
VOLUME /conf

# Copy source
COPY ha-appdaemon .

# INSTALL

RUN pip3 install .

CMD [ "appdaemon", "-c", "/conf" ]
