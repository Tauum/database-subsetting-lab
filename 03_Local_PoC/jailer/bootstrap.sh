#!/bin/sh
set -eu
mkdir -p /opt/jailer /work/models /work/exports /work/tmp
# Populate the host-mounted application directory on a fresh checkout.
# Preserve existing application files when the pinned Jailer JAR already matches.
if ! cmp -s /opt/jailer-dist/jailer.jar /opt/jailer/jailer.jar; then
  cp -a /opt/jailer-dist/. /opt/jailer/
fi
exec "$@"
