FROM node:20-alpine AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

RUN mkdir /app
WORKDIR /app

FROM base as build

COPY  ./package.json ./pnpm-lock.yaml ./

RUN pnpm i --shamefully-hoist

COPY --link ../ .

RUN pnpm build


FROM nginx:alpine
ENV NODE_ENV=production

ARG NGINX_DEFAULT=default.conf

RUN mkdir /app
WORKDIR /app

COPY --from=build /app/dist/ /app/
COPY .devcontainer/nginx/${NGINX_DEFAULT}  /etc/nginx/conf.d/default.conf
