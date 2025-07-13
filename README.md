# Сервис анализа отзывов

Мини-сервис для анализа настроения отзывов пользователей.

## Установка и запуск

```bash
git clone git@github.com:nepa27/ucar_test.git
cd ucar_test

pip install -r requirements.txt

python app.py
```

Сервис запустится на `http://localhost:5000`

## API Endpoints

### POST /reviews
Создает новый отзыв и анализирует его настроение.

**Запрос:**
```json
{
  "text": "Это отличный продукт!"
}
```

**Ответ:**
```json
{
  "id": 1,
  "text": "Это отличный продукт!",
  "sentiment": "positive",
  "created_at": "2025-07-13T10:30:00.123456"
}
```

### GET /reviews
Получает все отзывы или фильтрует по настроению.

**Параметры:**
- `sentiment` (optional): `positive`, `negative`, `neutral`

## Примеры curl-запросов

### Создание отзыва:
```bash
curl -X POST http://localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text": "Этот продукт просто отличный!"}'
```

### Создание негативного отзыва:
```bash
curl -X POST http://localhost:5000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text": "Это плохой продукт"}'
```

### Получение всех отзывов:
```bash
curl http://localhost:5000/reviews
```

### Получение только негативных отзывов:
```bash
curl http://localhost:5000/reviews?sentiment=negative
```

## База данных

Автоматически создается SQLite файл `reviews.db` с таблицей:

```sql
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    sentiment TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```
