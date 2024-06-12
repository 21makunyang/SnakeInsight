from flask_cors import CORS

from snake_insight_server.server import app


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 19198

    CORS(app)
    app.run(host=host, port=port)
