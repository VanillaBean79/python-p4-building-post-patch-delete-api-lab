#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()
    return make_response ( bakery_serialized, 200  )

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )


@app.route('/baked_goods', methods=['POST'])#set up route
def create_baked_good():#define method

    name = request.form.get('name')#get form data
    price = request.form.get('price')
    bakery_id = request.form.get('bakery_id')

    #create new data
    new_baked_good = BakedGood(
        name=name,
        price=price,
        bakery_id=bakery_id
    )

    db.session.add(new_baked_good)#add new data 
    db.session.commit()#commit to database

    baked_good_dict = new_baked_good.to_dict()#place data in dictionary
    #make a clarification that the data hase been saved.
    response = make_response(
        jsonify(baked_good_dict),
        201
    )
    #retrun response about data.
    return response


@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):  # Make sure the 'id' parameter is here
    # Retrieve the bakery by its ID
    bakery = db.session.get(Bakery, id)

    if not bakery:
        # Return a 404 error if the bakery is not found
        return jsonify({"error": "Bakery not found."}), 404

    # Loop through the form data and update the bakery's attributes
    for attr in request.form:
        setattr(bakery, attr, request.form.get(attr))

    # Commit the changes to the database
    db.session.commit()

    # Convert the updated bakery object to a dictionary
    bakery_dict = bakery.to_dict()

    # Return the updated bakery data as JSON with a 200 OK status code
    return make_response(bakery_dict, 200)


@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_goods(id):
    baked_good = db.session.get(BakedGood, id)
    if not baked_good:
        return jsonify({"error": "Baked good not found."})
    
    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({
        "delete_successful": True,
        "message": f"Baked good with id {id} deleted."
    }), 200


        


if __name__ == '__main__':
    app.run(port=5555, debug=True)