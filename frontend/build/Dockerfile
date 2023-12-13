# Use a node base image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install app dependencies
RUN npm install

# Bundle app source
COPY . .

# Build the app
RUN npm run build

# Install serve to run the application
RUN npm install -g serve

# The port that will be exposed
EXPOSE 3000

# Run the app
CMD ["serve", "-s", "build"]
