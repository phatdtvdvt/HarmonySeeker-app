FROM node:22.9.0

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose port (optional for dev)
EXPOSE 3000
