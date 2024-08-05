from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, Asset
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class AssetResource(Resource):
    def get(self, id=None):
        if id:
            asset = Asset.query.get_or_404(id)
            asset_data = {
                'id': asset.id,
                'user_id': asset.user_id,
                'name': asset.name,
                'value': str(asset.value),  
                'purchase_date': asset.purchase_date.strftime('%Y-%m-%d'),
                'description': asset.description,
                'created_at': asset.created_at,
                'updated_at': asset.updated_at
            }
            return jsonify({'asset': asset_data})
        else:
            assets = Asset.query.all()
            output = []
            for asset in assets:
                asset_data = {
                    'id': asset.id,
                    'user_id': asset.user_id,
                    'name': asset.name,
                    'value': str(asset.value),  
                    'purchase_date': asset.purchase_date.strftime('%Y-%m-%d'),
                    'description': asset.description,
                    'created_at': asset.created_at,
                    'updated_at': asset.updated_at
                }
                output.append(asset_data)
            return jsonify({'assets': output})

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')
        value = data.get('value')
        purchase_date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d')
        description = data.get('description')

        new_asset = Asset(
            user_id=user_id,
            name=name,
            value=value,
            purchase_date=purchase_date,
            description=description
        )
        db.session.add(new_asset)
        db.session.commit()

        return {'message': 'Asset created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        asset = Asset.query.get_or_404(id)

        asset.user_id = data.get('user_id', asset.user_id)
        asset.name = data.get('name', asset.name)
        asset.value = data.get('value', asset.value)
        asset.purchase_date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d') if data.get('purchase_date') else asset.purchase_date
        asset.description = data.get('description', asset.description)

        db.session.commit()

        return {'message': 'Asset updated successfully'}

    def delete(self, id):
        asset = Asset.query.get_or_404(id)
        db.session.delete(asset)
        db.session.commit()

        return {'message': 'Asset deleted successfully'}



if __name__ == '__main__':
    app.run(debug=True)