# Docker instructions to build a deployment Linux container.
#
# For more information, visit https://docs.docker.com/engine/reference/builder.

FROM node:24 AS build

WORKDIR /repo

RUN apt-get update && apt-get install --yes zip && npm install --global pnpm

COPY . .

RUN pnpm install --frozen-lockfile && pnpm exec vite build

FROM nginx:1.29

COPY --from=build /repo/build/dist /usr/share/nginx/html
