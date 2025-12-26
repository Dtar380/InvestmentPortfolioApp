# STAGE 1: Build Stage
FROM node:21 AS builder

# Set working directory
WORKDIR /app

# Install node dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application code and build the app
COPY . .

EXPOSE 3000
CMD [ "npm", "run", "dev" ]
