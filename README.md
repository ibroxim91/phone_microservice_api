# Phone-Address Microservice

## 📖 Описание
Микросервис для хранения и управления связками **"телефон-адрес"**.  
Сервис реализован на **FastAPI + Redis** и предоставляет REST API для работы с данными.

### 🎯 Цели
- Кеширование часто запрашиваемой информации
- Быстрая проверка наличия данных по номеру телефона
- Простая и правильная архитектура REST API

---

## ⚙️ Используемый стек
- **Python 3.11+**
- **FastAPI** — веб-фреймворк
- **Redis** — хранилище данных
- **Docker / Docker Compose** — контейнеризация

---

## 🚀 Запуск проекта

### 1. Клонирование репозитория
```bash
git clone https://github.com/ibroxim91/phone_microservice_api
cd phone-address-service



## Запуск через Docker Compose

```bash
docker-compose up --build
```

## После запуска сервис будет доступен по адресу:


http://localhost:8001

## Структура проекта

app/
 ├── main.py          # Точка входа FastAPI
 ├── routers/         # Маршруты (phone_router.py)
 ├── crud/            # Логика работы с Redis
 ├── schemas/         # Pydantic схемы
 ├── db.py            # Подключение к Redis
 └── Dockerfile       # Docker образ
docker-compose.yml    # Docker Compose конфигурация
README.md             # Документация
.env                  # envoriment


# 📌 REST API эндпоинты
## 1. Получение адреса по телефону
### GET /phone/{phone}

✅ Если найден → HTTP 200 + JSON: { "phone": "...", "address": "..." }

❌ Если не найден → HTTP 404

## 2. Создание новой записи
### POST /phone Тело запроса (JSON):

json
{
  "phone": "998901234567",
  "address": "Tashkent, Amir Temur street"
}
✅ Если создано → HTTP 201

❌ Если телефон уже существует → HTTP 409 (Conflict)

## 3. Обновление существующей записи
### PUT /phone/{phone} Тело запроса (JSON):

json
{
  "address": "New address"
}
✅ Если обновлено → HTTP 200

❌ Если телефон не найден → HTTP 404

## 4. Удаление записи (опционально)
### DELETE /phone/{phone}

✅ Если удалено → HTTP 204 (No Content)

❌ Если телефон не найден → HTTP 404