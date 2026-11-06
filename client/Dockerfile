FROM node:20-alpine AS builder
WORKDIR /app

# Copy package files relative to the ./client build context
COPY package*.json ./
RUN npm install

# Copy the remaining client source files
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]