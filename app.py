import yaml
from flask import Flask
from flasgger import Swagger
from extensions import db
from my_project.auth.controller.customer_controller import customer_bp
from my_project.auth.controller.account_controller import account_bp
from my_project.auth.controller.transaction_controller import transaction_bp
from my_project.auth.controller.card_controller import card_bp
from my_project.auth.controller.bankdetail_controller import bankdetail_bp
from my_project.auth.controller.customeraddress_controller import customeraddress_bp
from my_project.auth.controller.customeraccount_controller import customeraccount_bp
from my_project.auth.controller.column_stat_controller import stat_bp
from my_project.auth.controller.table_split_controller import split_accounts_bp

app = Flask(__name__)

swagger = Swagger(app)

with open("config/app.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

app.config['DEBUG'] = config['app']['debug']
app.config['SECRET_KEY'] = config['app']['secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = config['app']['database_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(customer_bp, url_prefix='/api')
app.register_blueprint(account_bp, url_prefix='/api')
app.register_blueprint(transaction_bp, url_prefix='/api')
app.register_blueprint(card_bp, url_prefix='/api')
app.register_blueprint(bankdetail_bp, url_prefix='/api')
app.register_blueprint(customeraddress_bp, url_prefix='/api')
app.register_blueprint(customeraccount_bp, url_prefix='/api')
app.register_blueprint(stat_bp, url_prefix='/api')
app.register_blueprint(split_accounts_bp, url_prefix='/api')

@app.route('/')
def home():
    """
    MAIN PAGE
    ---
    responses:
      200:
        description: Returns a message about the service status
    """
    return 'Flask app is running with config from app.yml!'

@app.errorhandler(404)
def not_found_error(error):
    """ 
    404 Error Handler
    ---
    responses:
      404:
        description: Resource not found
    """
    return {'message': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    """
    500 Error Handler
    ---
    responses:
      500:
        description: Internal server error
    """
    db.session.rollback()
    return {'message': 'Internal server error'}, 500

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
