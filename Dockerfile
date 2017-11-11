
FROM python:3.6
MAINTAINER Julian Kahnert <mail@juliankahnert.de>
LABEL org.freenas.version="2.1.12" \
      org.freenas.upgradeable="true" \
      org.freenas.autostart="true" \
      org.freenas.web-ui-protocol="http" \
      org.freenas.web-ui-port=5050 \
      org.freenas.web-ui-path="states" \
      org.freenas.expose-ports-at-host="true" \
      org.freenas.port-mappings="5050:5050/tcp" \
      org.freenas.volumes="[ \
          { \
              \"name\": \"/conf\", \
              \"descr\": \"HADashboard config\" \
          } \
      ]"\
      org.freenas.settings="[ \
          { \
              \"env\": \"TZ\", \
              \"descr\": \"homeassistant Container Timezone\", \
              \"optional\": true \
          } \
      ]"

VOLUME /conf
VOLUME /certs
EXPOSE 5050

# Copy appdaemon into image
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY haappdaemon/. .

# Install
RUN pip3 install .

# Start script
RUN chmod +x /usr/src/app/dockerStart.sh
CMD [ "./dockerStart.sh" ]
    