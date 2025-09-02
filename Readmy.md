# 🐳 Docker & PostgreSQL Шпаргалка

1. Остановить контейнеры (если они запущены)
docker-compose down

2. Удалить старые контейнеры и образы (чтобы гарантировать пересборку)
docker system prune -af

3. Пересобрать образы с нуля
docker-compose build --no-cache

4. Запустить контейнеры в фоне
docker-compose up -d

5. Проверить, что все сервисы работают
docker ps

не6. (Необязательно) посмотреть логи бота или API, если нужно
docker-compose logs -f bot
docker-compose logs -f api

### 🔍 Посмотреть список контейнеров
```bash
docker ps
```

### 📦 Все контейнеры (включая завершенные)
```bash
docker ps -a
```

### 📝 Посмотреть логи контейнера (например, почему упал)
```bash
docker logs <CONTAINER_ID>
```

### 📡 Следить за логами всех сервисов
```bash
docker-compose logs -f
```

### ▶️ Запустить контейнеры в фоне (не блокирует терминал)
```bash
docker-compose up -d
```

### ✅ Проверить запущенные контейнеры
```bash
docker-compose ps
```

### ⛔ Выключить все контейнеры
```bash
docker-compose down
```

### 🗑 Полностью удалить все контейнеры (остановленные и работающие)
```bash
docker rm -f $(docker ps -aq)
```

---

## 🐘 PostgreSQL

### 🔗 Сбилдить и запустить
```bash
docker-compose up --build
```

### 🔗 Подключиться к контейнеру PostgreSQL
```bash
docker exec -it <db> psql -U postgres -d astrodb
```

### 📋 Вывести все таблицы
```sql
\dt
```

### 🏗 Показать структуру таблицы
```sql
\d users
```

### 👤 Показать всех пользователей
```sql
SELECT * FROM users;
```

### 👤 Выйти из бд
```sql
\q
```

---

💡 **Совет:**  
Чтобы не запоминать `<CONTAINER_ID>`, используй:
```bash
docker ps
```
или имя контейнера, например:
```bash
docker exec -it db psql -U postgres -d astrodb
```
