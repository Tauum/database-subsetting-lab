# syntax=docker/dockerfile:1
# The tested Java runtime and official Jailer release are pinned.
FROM eclipse-temurin:21-jre@sha256:18bb4a91a3dea3f03ee31d3755af34dfb40f904fc77ab56cdc2f092e32fff9c2 AS unpack
ADD --checksum=sha256:0cd07186ba9464f37d384c0fd8a68b00d1e4b2eb3900c98e540bc692901317b4 https://github.com/Wisser/Jailer/releases/download/v17.3.1/jailer_17.3.1.zip /tmp/jailer.zip
RUN apt-get update && apt-get install -y --no-install-recommends unzip && mkdir /unpacked && unzip -q /tmp/jailer.zip -d /unpacked

FROM eclipse-temurin:21-jre@sha256:18bb4a91a3dea3f03ee31d3755af34dfb40f904fc77ab56cdc2f092e32fff9c2
COPY --from=unpack /unpacked/jailer/ /opt/jailer-dist/
COPY bootstrap.sh /usr/local/bin/jailer-bootstrap.sh
WORKDIR /opt/jailer
ENTRYPOINT ["sh", "/usr/local/bin/jailer-bootstrap.sh"]
CMD ["sleep", "infinity"]
