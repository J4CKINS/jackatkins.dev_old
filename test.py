import sys
from __init__ import app

if __name__ == "__main__":
    app.config['SERVER_NAME'] = f'jackatkins.test:{str(sys.argv[1])}'
    app.run(debug=True)
