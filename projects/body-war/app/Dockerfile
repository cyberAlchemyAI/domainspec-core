# syntax=docker/dockerfile:1

FROM node:22-alpine AS deps
WORKDIR /workspace

COPY projects/auth-user-management/package*.json ./projects/auth-user-management/
COPY projects/body-war/app/package*.json ./projects/body-war/app/

RUN npm ci --prefix projects/auth-user-management \
  && npm ci --prefix projects/body-war/app

FROM node:22-alpine AS build
WORKDIR /workspace

COPY --from=deps /workspace/projects/auth-user-management/node_modules ./projects/auth-user-management/node_modules
COPY --from=deps /workspace/projects/body-war/app/node_modules ./projects/body-war/app/node_modules
COPY projects/auth-user-management ./projects/auth-user-management
COPY projects/body-war/app ./projects/body-war/app

RUN npm --prefix projects/body-war/app run build

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /workspace/projects/body-war/app

COPY --from=deps /workspace/projects/body-war/app/node_modules ./node_modules
COPY --from=deps /workspace/projects/auth-user-management/node_modules /workspace/projects/auth-user-management/node_modules
COPY --from=build /workspace/projects/auth-user-management/dist /workspace/projects/auth-user-management/dist
COPY --from=build /workspace/projects/auth-user-management/drizzle /workspace/projects/auth-user-management/drizzle
COPY --from=build /workspace/projects/auth-user-management/package.json /workspace/projects/auth-user-management/package.json
COPY --from=build /workspace/projects/body-war/app/dist ./dist
COPY --from=build /workspace/projects/body-war/app/drizzle ./drizzle
COPY --from=build /workspace/projects/body-war/app/static ./static
COPY --from=build /workspace/projects/body-war/app/package.json ./package.json

EXPOSE 5174
CMD ["node", "dist/server.js"]
