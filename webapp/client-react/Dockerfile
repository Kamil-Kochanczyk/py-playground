FROM node:24-slim AS common

WORKDIR /usr/src/app/

COPY package*.json ./

RUN --mount=type=cache,target=/usr/src/app/.npm \
  npm set cache /usr/src/app/.npm && \
  npm install

COPY ./ ./



FROM common AS dev

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]



FROM common AS builder

RUN npm run build



FROM nginx:1.31.6-alpine-slim AS prod

# --link is used to put files on an independent layer,
# i.e. a layer which doesn't get invalidated when commands on previous layers change
COPY --link nginx.conf /etc/nginx/conf.d/default.conf

# this way the "--link"-ed files here can be reused even if the base nginx image changes
# this is because they are basically independent from this base image
COPY --link --from=builder /usr/src/app/dist/ /usr/share/nginx/html

# create a writable PID/cache directory and ensure the nginx user owns it
# without this, the non-root user cannot create /run/nginx.pid and the container exits
# -p is for creating parent directories as needed
# -R is for recursive, so it applies to all subdirectories and files
RUN mkdir -p /run /tmp/nginx /var/cache/nginx /var/run /var/log/nginx && \
    chown -R nginx:nginx /run /tmp/nginx /usr/share/nginx/html /var/cache/nginx /var/run /var/log/nginx

# changing to non-root user is less critical than in the node image
# this is because nginx serves read-only static files
USER nginx

EXPOSE 8080

# you could also write CMD instead of ENTRYPOINT here
# if you wrote CMD here you could overrride the nginx command at "docker run" time
# by using ENTRYPOINT you fix the runtime to always run nginx command
# in this way you pinpoint the behaviour to one specific command
# you can still override it, though, with "--entrypoint ..." flag
ENTRYPOINT [ "nginx", "-g", "daemon off;" ]
