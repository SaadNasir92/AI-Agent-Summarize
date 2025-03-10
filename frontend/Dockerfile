FROM node:14

WORKDIR /app

# Copy package.json and install dependencies
COPY package.json .
RUN npm install

# Copy the rest of the frontend code
COPY . .

# By default, run the dev server on port 3000
CMD ["npm", "start"]
