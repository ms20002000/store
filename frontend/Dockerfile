# Use a lightweight web server image
FROM nginx:alpine

# Copy React build files to the Nginx web root
COPY . /usr/share/nginx/html

# Expose port 80 for the container
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
