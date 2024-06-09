from flask import Flask, request, make_response

from .Filter import Filter
from .route import get_info, app

__all__ = ['app', 'request', 'make_response', 'Filter']



# app.route('/plot', methods=["GET", "POST"])(get_info)
