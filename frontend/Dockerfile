# Use an official Node.js runtime as the base image
FROM node:16-alpine as builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the entire project to the working directory
COPY public/ public/
COPY src/ src/

# Build the React app
RUN npm run build


# Use an official Nginx image as the base image
FROM nginx:1.21-alpine

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*

COPY --from=builder /app/build .

ENTRYPOINT ["nginx", "-g"]

# Expose the port on which the app will run
EXPOSE 80

# Define the command to run the app
CMD ["daemon off;"]