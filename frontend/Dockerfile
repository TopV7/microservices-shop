# Берем готовый образ Nginx
FROM nginx:alpine

# Копируем наш конфиг внутрь контейнера
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Копируем наш index.html в папку, из которой Nginx раздает файлы
COPY index.html /usr/share/nginx/html/index.html