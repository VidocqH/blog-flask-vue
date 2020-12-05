from flask import jsonify, request, url_for, g
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from app.models import Post

@bp.route('/posts', methods=['POST'])
@token_auth.login_required
def create_post():
    ''' Add a new post '''
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title'):
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'body' not in data or not data.get('body'):
        message['body'] = 'Body is required.'
    if message:
        return bad_request(message)

    post = Post()
    post.from_dict(data)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_post', id=post.id)
    return response

@bp.route('/posts', methods=['GET'])
def get_posts():
    ''' return sets of posts with paginate '''
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Post.to_collection_dict(Post.query.order_by(Post.timestamp.desc()), page, per_page, 'api.get_posts')
    return jsonify(data)

@bp.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    ''' return a post '''
    post = Post.query.get_or_404(id)
    post.views += 1
    db.session.add(post)
    db.session.commit()
    response = jsonify(post.to_dict())
    return response

@bp.route('/posts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_post(id):
    ''' modify a post '''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return error_response(403)

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    message = {}
    if 'title' not in data or not data.get('title'):
        message['title'] = 'Title is required.'
    elif len(data.get('title')) > 255:
        message['title'] = 'Title must less than 255 characters.'
    if 'body' not in data or not data.get('body'):
        message['body'] = 'Body is required.'
    if message:
        return bad_request(message)

    post.from_dict(data)
    db.session.commit()
    return jsonify(post.to_dict())

@bp.route('/posts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_post(id):
    ''' delete a post '''
    post = Post.query.get_or_404(id)
    if g.current_user != post.author:
        return error_response(403)
    db.session.delete(post)
    db.session.commit()
    return '', 204