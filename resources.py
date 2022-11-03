import json
from flask_restful import Resource
from flask import make_response, jsonify, request
from models import User, Address, Relation
from db_connections import db


class UserResource(Resource):
    def get(self):
        users = db.session.query(User).all()
        # _dicts = []
        # for user in users:
        #     _dicts.append({
        #         "id": user.id,
        #         "first_name": user.first_name,
        #         "last_name": user.last_name,
        #         "user_type": user.user_type
        #     })

        return make_response(jsonify({"helllo": 123}), 200)

    def post(self):
        data = request.get_json()
        user = User()
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.user_type = data.get("user_type")
        address = data.get("address")
        if user.user_type == "child" and address is not None:
            return make_response(jsonify({'message ': 'child cannot have address'}), 201)
        else:
            db.session.add(user)
            if user.user_type == "child":
                parent_id = data.get("parent_id")
                parent = User.query.filter(db.and_(User.id == parent_id, User.user_type == 'parent')).first()
                if parent is None:
                    return make_response(jsonify({'message ': 'there is no parent user with this name'}), 201)
                else:
                    db.session.commit()
                    relation = Relation()
                    relation.child_id = user.id
                    relation.parent_id = parent_id
                    db.session.add(relation)
            elif user.user_type == "parent":
                db.session.commit()
                address = Address(**address)
                address.user_id = user.id
                db.session.add(address)
        db.session.commit()
        return make_response(jsonify({'message ': 'saved'}), 200)

    def delete(self):
        data = request.get_json()
        user_id = data.get("user_id")
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        print(user.id)
        relations = Relation.query.filter(Relation.parent_id == user.id).all()
        for relation in relations:
            if relation is not None:
                child = User.query.filter(User.id == relation.child_id).first()
                db.session.delete(child)
                db.session.delete(relation)
                db.session.commit()
        return make_response(jsonify({'message ': 'deleted'}), 200)

    def put(self):
        data = request.get_json()
        id = data.get("user_id")
        user = User.query.get(id)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        db.session.commit()
        return make_response(jsonify({'message ': "updated"}), 200)


class ParentIdResource(Resource):
    def get(self):
        parents = User.query.filter(User.user_type == 'parent').all()
        parent_ids = []
        for parent in parents:
            parent_ids.append(parent.id)
        return make_response(jsonify(parent_ids), 200)


class ChildIdResource(Resource):
    def get(self):
        childs = User.query.filter(User.user_type == 'child').all()
        child_ids = []
        for child in childs:
            child_ids.append(child.id)
        return make_response(jsonify(child_ids), 200)


class UserInfo(Resource):
    def get(self, user_id):
        user = User.query.options(db.joinedload(User.address)).get(user_id)
        _dict = {}
        _dict.update({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_type": user.user_type
        })
        for address in user.address:
            _dicta = {}
            _dicta.update({
                "street": address.street,
                "state": address.state,
                "city": address.city,
                "zip": address.zip
            })
            _dict.update({
                "address": _dicta
            })
        return make_response(jsonify(_dict), 200)


class ParentResource(Resource):
    def get(self, parent_id):
        user = User.query.options(db.joinedload(User.address)).get(parent_id)
        if user.user_type == 'parent':
            _dict = {}
            _dict.update({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": user.user_type
            })
            for address in user.address:
                _dicta = {}
                _dicta.update({
                    "street": address.street,
                    "state": address.state,
                    "city": address.city,
                    "zip": address.zip
                })
                _dict.update({
                    "address": _dicta
                })
            childs = Relation.query.filter(Relation.parent_id == user.id).all()
            if childs.count(self) == 0:
                _dict.update({
                    "child ids": "No child"
                })
            else:
                _list = []
                for child in childs:
                    _list = [child.child_id]
                _dict.update({
                    "child ids": _list
                })

            return make_response(jsonify(_dict), 200)
        else:
            return make_response(jsonify({"message": "given id is not a parent"}), 201)


class ChildResource(Resource):
    def get(self, child_id):
        user = User.query.options(db.joinedload(User.child)).get(child_id)
        if user.user_type == "child":
            _dict = {}
            _dict.update({
                "first_name": user.first_name,
                "last_name": user.last_name,
                "user_type": user.user_type
            })
            for child in user.child:
                parent = User.query.filter(User.id == child.parent_id).first()
                _dictp = {}
                _dictp.update({
                    "id": parent.id,
                    "first_name": parent.first_name,
                    "last_name": parent.last_name
                })
                _dict.update({
                    "parent": _dictp
                })
            return make_response(jsonify(_dict), 200)
        else:
            return make_response(jsonify({"message": "given id is not a child"}), 201)
