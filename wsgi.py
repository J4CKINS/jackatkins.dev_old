from __init__ import app

if __name__ == "__main__":
    app.config['SERVER_NAME'] = 'jackatkins.test:80'
    app.run()