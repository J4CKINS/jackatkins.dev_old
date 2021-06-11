from __init__ import app

if __name__ == "__main__":
    app.config['SERVER_NAME'] = 'jackatkins.test:8000'
    app.run(debug=True)
