FROM node:20-slim AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN npm install -g corepack@latest

RUN corepack enable 
RUN corepack install --global pnpm@9.8.0
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0

COPY . /frontend
WORKDIR /frontend

EXPOSE 3075
