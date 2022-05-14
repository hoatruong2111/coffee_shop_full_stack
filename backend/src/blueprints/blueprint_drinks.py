from functools import wraps
from flask import Flask, request, jsonify, abort
import json
from .errors_handler import not_found
from ..auth.auth import requires_auth
from flask import Blueprint
from ..database.models import Drink

blueprint_drinks = Blueprint('blueprint_drinks', __name__)

PERMISSON = {
    "CAN_GET_DETAIL": "get:drinks-detail",
    "CAN_POST": "post:drinks",
    "CAN_PATCH": "patch:drinks",
    "CAN_DELETE": "delete:drinks",
}


def bindData(collection):
    result = []
    for col in collection:
        res = {
            "id": col.id,
            "title": col.title,
            "recipe": json.loads(col.recipe),
        }
        result.append(res)
    return result


@blueprint_drinks.route("/drinks")
def get_drinks():
    try:
        result = []
        drinks = Drink.query.order_by(Drink.id).all()
        for drink in drinks:
            val = drink.short()
            result.append(val)

        return jsonify({
            'drinks': result,
            'status': 200,
            'success': True
        })
    except Exception as e:
        abort(404)


@blueprint_drinks.route("/drinks-detail")
@requires_auth(PERMISSON['CAN_GET_DETAIL'])
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.order_by(Drink.id).all()
        result = bindData(drinks)
        return jsonify({
            'drinks': result,
            'status': 200,
            'success': True
        })
    except Exception as e:
        abort(404)


@blueprint_drinks.route("/drinks", methods=['POST'])
@requires_auth(PERMISSON["CAN_POST"])
def add_drink(payload):
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_recipe = body.get("recipe")
        drink = Drink(title=new_title, recipe=json.dumps(new_recipe))

        drink.insert()
        result = bindData([drink])
        return jsonify({
            "success": True,
            "drinks": result
        }
        )

    except Exception as e:
        abort(422)


@blueprint_drinks.route("/drinks/<int:drink_id>", methods=['PATCH'])
@requires_auth(PERMISSON["CAN_PATCH"])
def update_drink(payload, drink_id):
    try:
        body = request.get_json()
        new_title = body.get("title")
        new_recipe = body.get("recipe")
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink.title = new_title
        drink.recipe = json.dumps(new_recipe)

        drink.update()
        result = bindData([drink])
        return jsonify({
            "success": True,
            "drinks": result
        }
        )

    except Exception as e:
        abort(422)


@blueprint_drinks.route("/drinks/<int:drink_id>", methods=['DELETE'])
@requires_auth(PERMISSON["CAN_DELETE"])
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

        if drink is None:
            return not_found(404)

        drink.delete()

        return jsonify(
            {
                "success": True,
                "delete": drink_id
            }
        )

    except Exception as e:
        abort(422)
