from flask import jsonify, request
from flask_jwt import jwt_required
from models import User, db
from . import api

@api.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    if request.method == 'POST':
        print(request)
        data = request.get_json()
        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re-password')

        if not (userid and username and password and re_password):
            return jsonify({'ERROR': 'NO ARGUMENTS'}), 400

        if password != re_password:
            return jsonify({'ERROR': 'WRONG PASSWORD'}), 400

        user = User()
        user.userid = userid
        user.username = username
        user.password = password

        db.session.add(user)
        db.session.commit()

        return jsonify(), 201

    users = User.query.all()

    return jsonify([user.serialize for user in users])

@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = User.query.filter(User.id == uid).first()
        return jsonify(user.serialize)
    elif request.method == 'DELETE':
        User.query.delete(User.id == uid)
        return jsonify(), 204
    else:
        data = request.get_json()

        User.query.filter(User.id == uid).update(data)
        user = User.query.filter(User.id == uid).first()
        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize) 

