# [STAGE 1] Build Stage
FROM node:20-alpine AS build

WORKDIR /app

# 의존성 설치 최적화를 위한 복사
COPY package.json package-lock.json ./
RUN npm install

# 전체 소스 복사 및 빌드
COPY . .
RUN npm run build

# [STAGE 2] Production Stage
FROM nginx:stable-alpine

# 빌드 결과물 복사
COPY --from=build /app/dist /usr/share/nginx/html

# 커스텀 Nginx 설정 적용
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
