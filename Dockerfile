# Use the official Node.js runtime as the base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Copy backend requirements first to leverage Docker cache
COPY backend/requirements.txt ./backend/requirements.txt

# Install Python dependencies
RUN apk add --no-cache --virtual .build-deps build-base python3-dev && \
    pip install --no-cache-dir --break-system-packages -r backend/requirements.txt && \
    apk del .build-deps

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install ALL dependencies (needed for build)
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN npm run build

# Prune dev dependencies after build (optional, saves space)
RUN npm prune --production

# Expose the port the app runs on
EXPOSE 5000

# Set environment variable for production
ENV NODE_ENV=production
ENV PORT=5000

# Define the command to run the application
CMD ["npm", "start"]