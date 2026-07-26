FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY --chown=101:101 --chmod=444 deploy/nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=101:101 site/ /usr/share/nginx/html/
# nginx-unprivileged listens on 8080 as uid 101, no root anywhere
