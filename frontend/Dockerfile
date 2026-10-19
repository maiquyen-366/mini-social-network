# Stage 1: Base
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./
RUN npm install

# Stage 2: Development (dùng cho docker compose khi lập trình)
FROM base AS development
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

# Stage 3: Build static files cho production
FROM base AS build
ARG VITE_API_BASE_URL=http://localhost:8000/api
ARG VITE_WS_BASE_URL=ws://localhost:8000
ARG VITE_BACKEND_ORIGIN=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_WS_BASE_URL=$VITE_WS_BASE_URL
ENV VITE_BACKEND_ORIGIN=$VITE_BACKEND_ORIGIN
COPY . .
RUN npm run build

# Stage 4: Production (dùng Nginx phục vụ SPA)
FROM nginx:alpine AS production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
