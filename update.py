#!/usr/bin/env python3
import os
import subprocess
import haappdaemon.appdaemon.conf as appconf

subprocess.run(['git', 'submodule', 'update', '--recursive', '--remote'])
version = appconf.__version__

# get local tags
raw = subprocess.run(['git', 'tag'], stdout=subprocess.PIPE)
tags_local = raw.stdout.decode('utf-8').split('\n')[:-1]
tags_local += ['latest']
tags_local += ['dev']
tags_local = set(tags_local)

if version not in tags_local:
    print('\nprocessing version: {}\n'.format(version))

    dockerfile = """
FROM python:3.6
MAINTAINER Julian Kahnert <mail@juliankahnert.de>
LABEL org.freenas.version="{}" \\
      org.freenas.upgradeable="true" \\
      org.freenas.autostart="true" \\
      org.freenas.web-ui-protocol="http" \\
      org.freenas.web-ui-port=5050 \\
      org.freenas.web-ui-path="states" \\
      org.freenas.expose-ports-at-host="true" \\
      org.freenas.port-mappings="5050:5050/tcp" \\
      org.freenas.volumes="[ \\
          {{ \\
              \\"name\\": \\"/conf\\", \\
              \\"descr\\": \\"HADashboard config\\" \\
          }} \\
      ]"\\
      org.freenas.settings="[ \\
          {{ \\
              \\"env\\": \\"TZ\\", \\
              \\"descr\\": \\"homeassistant Container Timezone\\", \\
              \\"optional\\": true \\
          }} \\
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
    """.format(version)
    f = open('Dockerfile', 'w')
    f.write(dockerfile)
    f.close()

    # v="0.42" && git commit --all --message "Version $v" && git tag $v && git push --tags
    subprocess.run(['git', 'commit', '--all', '--message', 'Version {}'.format(version)])
    subprocess.run(['git', 'tag', version])
    subprocess.run(['git', 'push', '--tags', 'public', 'master'])
