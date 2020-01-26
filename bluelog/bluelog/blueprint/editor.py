# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required
from bluelog.models import Category, Post
from bluelog.extensions import db
from flask_cors import CORS

editor_bp = Blueprint('editor', __name__)
CORS(editor_bp)


@editor_bp.route('/get_categories')
def get_categories():
    items = Category.query.order_by(Category.name).all()
    data = []
    for item in items:
        ans = {
            'id': item.id,
            'name': item.name
        }
        data.append(ans)

    return jsonify({'data': data})


@editor_bp.route('/get_post', methods=['POST'])
def get_post():
    data = request.get_json()
    if data is None or data.get('title') is None or data.get('category_id') is None or data.get('body') is None:
        return jsonify({'message': 'Invalidate data', 'type': 'error'})
    category = Category.query.get(data.get('category_id'))
    post = Post(title=data.get('title'), category=category, body=data.get('body'))
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Create Success', 'type': 'success'})


@editor_bp.route('/create')
@login_required
def editor():
    return render_template('index.html')
