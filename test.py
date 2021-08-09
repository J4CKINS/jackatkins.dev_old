import sys
from __init__ import app

if __name__ == "__main__":
    app.config['SERVER_NAME'] = f'{sys.argv[1]}:{str(sys.argv[2])}'
    app.run(debug=True)
