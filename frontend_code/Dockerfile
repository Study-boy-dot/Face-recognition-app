# Use the official NGINX image as the base image
FROM nginx:latest

# Copy the custom nginx configuration file to the container
# COPY nginx.conf.template /nginx.conf.template
COPY nginx.conf /etc/nginx/conf.d/default.conf.template
COPY entrypoint.sh /entrypoint.sh

# Copy the static HTML and JavaScript files to the NGINX html directory
COPY index.html /usr/share/nginx/html/index.html
COPY upload.js /usr/share/nginx/html/upload.js

# Expose port 80 to the outside world
EXPOSE 80

# Start NGINX when the container launches
# CMD ["/bin/sh" , "-c" , "envsubst < /nginx.conf.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'"]
# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
