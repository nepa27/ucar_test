from datetime import datetime
import sqlite3

from flask import Flask, request, jsonify


app = Flask(__name__)

POSITIVE_WORDS = (
    'хорош',
    'отличн',
    'супер',
    'люблю',
    'нравится',
    'крут',
    'замечательн',
    'прекрасно',
)
NEGATIVE_WORDS = (
    'плох',
    'ужасн',
    'ненавиж',
    'отвратительно',
    'кошмар',
    'бред',
    'жесть',
    'нехорош'
)


def init_db():
    """Инициализация базы данных."""
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
                   CREATE TABLE IF NOT EXISTS reviews (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          text TEXT NOT NULL,
                                                          sentiment TEXT NOT NULL,
                                                          created_at TEXT NOT NULL
                   )
                   '''
    )
    conn.commit()
    conn.close()


def analyze_sentiment(text: str) -> str:
    """Анализ настроения."""
    text_lower = text.lower().split()

    for word in NEGATIVE_WORDS:
        if any(w.startswith(word) for w in text_lower):
            return 'negative'

    for word in POSITIVE_WORDS:
        if any(w.startswith(word) for w in text_lower):
            return 'positive'

    return 'neutral'


@app.route('/reviews', methods=['POST'])
def create_review():
    """Создание нового отзыва."""
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({'error': 'Поле text обязательно'}), 400

        text = data['text']
        sentiment = analyze_sentiment(text)
        created_at = datetime.utcnow().isoformat()

        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
            (text, sentiment, created_at),
        )
        review_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return (
            jsonify(
                {
                    'id': review_id,
                    'text': text,
                    'sentiment': sentiment,
                    'created_at': created_at,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reviews', methods=['GET'])
def get_reviews():
    """Получение отзывов с фильтрацией по настроению."""
    try:
        sentiment_filter = request.args.get('sentiment')

        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()

        if sentiment_filter:
            cursor.execute(
                'SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ?',
                (sentiment_filter,),
            )
        else:
            cursor.execute(
                'SELECT id, text, sentiment, created_at FROM reviews'
            )

        reviews = []
        for row in cursor.fetchall():
            reviews.append(
                {
                    'id': row[0],
                    'text': row[1],
                    'sentiment': row[2],
                    'created_at': row[3],
                }
            )

        conn.close()
        return jsonify(reviews)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


init_db()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
