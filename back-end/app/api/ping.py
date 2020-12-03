from flask import jsonify
from app.api import bp

@bp.route('/ping', methods=['GET'])
def ping():
    ''' Ping Test ''' 
    return jsonify('Pong!')