from flask import Flask, request, make_response

from .route import get_info

app = Flask(__name__)

__all__ = ['app', 'request', 'make_response']


app.route('/plot', methods=["GET", "POST"])(get_info)
