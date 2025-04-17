FROM nginx:latest

# Создание директории для статических файлов
RUN mkdir -p /app/staticfiles

# Копирование конфигурации Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копирование HTML-файлов (если необходимо)
COPY html/ /usr/share/nginx/html/

# Установка прав доступа к директории staticfiles
RUN chmod -R 755 /app/staticfiles/
RUN chown -R www-data:www-data /app/staticfiles/

# Открыть порт
EXPOSE 80