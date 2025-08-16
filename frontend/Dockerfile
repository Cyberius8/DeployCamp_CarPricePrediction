FROM nginx:alpine
COPY index.html /etc/nginx/html/index.html
COPY styles.css /etc/nginx/html/styles.css
COPY images/carprice.ico /etc/nginx/html/images/carprice.ico
COPY too_many_requests.html /etc/nginx/html/too_many_requests.html
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
