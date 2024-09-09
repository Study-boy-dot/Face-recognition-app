#!/bin/sh

# Substitute environment variables in the nginx configuration file
envsubst '${BACKEND_SERVICE_NAME} ${BACKEND_SERVICE_PORT}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Start nginx
nginx -g 'daemon off;'

