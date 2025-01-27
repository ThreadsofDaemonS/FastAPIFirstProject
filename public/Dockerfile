# Базовый образ Node.js
FROM node:18

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь проект
COPY . .

# Собираем проект
RUN npm run build

# Устанавливаем сервер для статических файлов
RUN npm install -g serve

# Указываем порт
EXPOSE 8080

# Запускаем сервер
CMD ["serve", "-s", "dist"]
