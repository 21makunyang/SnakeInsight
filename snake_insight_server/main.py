from snake_insight_server.server import app


if __name__ == '__main__':
    host = 'localhost'
    port = 19198

    app.run(host=host, port=port)
