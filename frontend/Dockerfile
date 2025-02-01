FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY . /uno
WORKDIR /uno

FROM base AS dev-uno
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install

FROM base
COPY --from=dev-uno /uno/node_modules /uno/node_modules

EXPOSE 3075

CMD [ "pnpm", "start" ]
