from app import app


if __name__ == '__main__':
    # gunicorn --bind 0.0.0.0:5000 wsgi:app
    app.run(host="0.0.0.0", port=5000)
