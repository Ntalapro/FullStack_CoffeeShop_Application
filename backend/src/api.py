import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc , desc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
#db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
@requires_auth("get:drinks")
def retrieve_drinks():
        print(" in here!")
        try:
            drinks = Drink.query.order_by(Drink.id).all()
            short_drinks = [drinks.short() for drink in drinks]
            
            return jsonify(
            {
                "success": True,
                "drinks": short_drinks
            }
        )
        except:
            abort(500)
        

'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth("get:drinks-detail")
def retrieve_drinks_detail(payload):
        print("long_drinks in here")
        try:
            drinks = Drink.query.order_by(Drink.id).all()
            long_drinks = [drink.long() for drink in drinks]

            return jsonify(
            {
                "success": True,
                "drinks": long_drinks
            }
        )
        except:
            abort(404)
        

'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def add_drink(payload):
    body = request.get_json()

    title= body.get("title", None)
    recipe = str(body.get("recipe", None)).replace("'", '"')
        
    try:
        drink = Drink(title=title, recipe =recipe)
        drink.insert()

        drink_ = Drink.query.order_by(desc(Drink.id)).all()[0]

        return jsonify(
                    {
                        "success": True, 
                        "drinks": drink_.long()
                    }
                )
    except:
        abort(422)



'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def patch_drink(payload,id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink == None:
            abort(404)
        else:
            drink.title = 'Black Coffee'
            drink.update()

            return jsonify(
                    {
                        "success": True, 
                        "drinks": drink.long()
                    }
                )
    except:
        abort(422)



'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("patch:drinks")
def delete_drink(payload,id):
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink != None:
            drink.delete()

            return jsonify(
            {
                "success": True,
                "deleted": id,
            }
        )
        else:
            abort(404)
        
            

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
        return jsonify({
            "success": False,
            "error":404,
            "message" : "resource not found"
        }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(403)
def forbidden(error):
        return jsonify({
            "success": False,
            "error":403,
            "message" : "You don’t have permission"
        }), 403
