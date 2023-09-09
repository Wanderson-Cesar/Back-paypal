from flask import Flask
from flask_cors import CORS
from database import db, migrate
from routes.payment_routes import payment_bp  


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123@localhost:5432/DBpaypal"
db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(payment_bp)

if __name__ == '__main__':
    app.run(debug=True)
