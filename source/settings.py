from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, Setting, User
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class SettingResource(Resource):
    def get(self, id=None):
        if id:
            setting = Setting.query.get_or_404(id)
            setting_data = {
                'id': setting.id,
                'user_id': setting.user_id,
                'setting_name': setting.setting_name,
                'setting_value': setting.setting_value,
                'created_at': setting.created_at,
                'updated_at': setting.updated_at
            }
            return jsonify({'setting': setting_data})
        else:
            settings = Setting.query.all()
            output = []
            for setting in settings:
                setting_data = {
                    'id': setting.id,
                    'user_id': setting.user_id,
                    'setting_name': setting.setting_name,
                    'setting_value': setting.setting_value,
                    'created_at': setting.created_at,
                    'updated_at': setting.updated_at
                }
                output.append(setting_data)
            return jsonify({'settings': output})

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        setting_name = data.get('setting_name')
        setting_value = data.get('setting_value')

        new_setting = Setting(
            user_id=user_id,
            setting_name=setting_name,
            setting_value=setting_value
        )
        db.session.add(new_setting)
        db.session.commit()

        return {'message': 'Setting created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        setting = Setting.query.get_or_404(id)

        setting.user_id = data.get('user_id', setting.user_id)
        setting.setting_name = data.get('setting_name', setting.setting_name)
        setting.setting_value = data.get('setting_value', setting.setting_value)
        setting.updated_at = datetime.utcnow()

        db.session.commit()

        return {'message': 'Setting updated successfully'}

    def delete(self, id):
        setting = Setting.query.get_or_404(id)
        db.session.delete(setting)
        db.session.commit()

        return {'message': 'Setting deleted successfully'}

api.add_resource(SettingResource, '/settings', '/settings/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
