# STAGE 1: Build Stage
FROM node:21 AS builder

# Set working directory
WORKDIR /app

# Install node dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy application code and build the app
COPY . .
RUN npm run build

# STAGE 2: Runtime Stage
FROM nginx:alpine AS runtime

# Copy built files from the builder stage and nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port and run the application
EXPOSE 80
CMD [ "nginx", "-g", "daemon off" ]
