FROM node:20-slim AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

RUN npm install -g corepack@latest

RUN corepack enable 
RUN corepack install --global pnpm@9.8.0
ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0

COPY . /csg
WORKDIR /csg

FROM base AS dev-csg
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install

FROM base
COPY --from=dev-csg /csg/node_modules /csg/node_modules

EXPOSE 3075

CMD [ "pnpm", "start" ]
