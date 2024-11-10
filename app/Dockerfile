ARG NODE_IMAGE=node:latest

FROM $NODE_IMAGE as base

RUN mkdir -p /home/node/app && chown node:node /home/node/app
WORKDIR /home/node/app
USER node

FROM base as dependencies
COPY --chown=node:node ./package*.json ./
COPY --chown=node:node . .
RUN rm -rf node_modules
RUN rm package-lock.json

ENV NODE_ENV=development

RUN npm install