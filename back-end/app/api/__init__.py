from flask import Blueprint

bp = Blueprint('api', __name__)

# Prevent recursive loop
from app.api import ping, users, tokens, posts, comments