
FROM node:16

WORKDIR /app

COPY package*.json ./
COPY package-lock.json ./

RUN npm install

COPY . ./

# EXPOSE 3000
RUN npm run build

# CMD ["npm", "start"]

# Stage 2: Serve
FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]