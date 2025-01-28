# Base Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the entire project
COPY . .

# Build the project
RUN npm run build

# Install a static file server
RUN npm install -g serve

# Specify the port
EXPOSE 8080

# Start the server
CMD ["serve", "-s", "dist"]
