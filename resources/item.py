from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="price field cannot be left blank."
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="store_id field cannot be left blank."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 # 400 bad request
        #data = request.get_json()
        data = Item.parser.parse_args()
        
        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting an item."}, 500 #internal server error 200 is default that blames user
        
        return item.json(), 201 # 201 created status msg

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item deleted'}
        return {'message': 'item not found for deletion'}, 404

    def put(self, name):
        #data = request.get_json()
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else: 
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}