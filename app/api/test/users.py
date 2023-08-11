from flask import jsonify, request, current_app, url_for
from app.api.test import test
from app.models.UserModel import User


@test.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

