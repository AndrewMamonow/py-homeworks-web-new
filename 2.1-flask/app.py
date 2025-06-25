from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    owner = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'owner': self.owner
        }

# Создание таблиц
db.create_all()

# Роут для работы с объявлениями
@app.route('/ads', methods=['POST', 'GET'])

def manage_ads():
    if request.method == 'POST': # Создание объявления
        data = request.get_json()
        new_ad = Ad(
            title=data.get('title'),
            description=data.get('description'),
            owner=data.get('owner')
        )
        db.session.add(new_ad)
        db.session.commit()
        return jsonify(new_ad.to_dict()), 201

    elif request.method == 'GET': # Получение всех объявлений
        ads = Ad.query.all()
        return jsonify([ad.to_dict() for ad in ads])

@app.route('/ads/<int:ad_id>', methods=['GET', 'DELETE'])

def ad_operations(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    
    if request.method == 'GET': # Получение объявления
        return jsonify(ad.to_dict())
    
    elif request.method == 'DELETE': # Удаление объявления
        db.session.delete(ad)
        db.session.commit()
        return jsonify({'message': 'Объявление удалено'})

if __name__ == '__main__':
    app.run(debug=True)