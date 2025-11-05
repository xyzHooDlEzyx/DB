import logging

from flask import Flask
from flasgger import Swagger
from flask_basicauth import BasicAuth
from flask_cors import CORS

from config.config import Config
from extensions import db
from my_project.auth.controller.account_controller import account_bp
from my_project.auth.controller.bankdetail_controller import bankdetail_bp
from my_project.auth.controller.card_controller import card_bp
from my_project.auth.controller.column_stat_controller import stat_bp
from my_project.auth.controller.customer_controller import customer_bp
from my_project.auth.controller.customeraccount_controller import customeraccount_bp
from my_project.auth.controller.customeraddress_controller import customeraddress_bp
from my_project.auth.controller.table_split_controller import split_accounts_bp
from my_project.auth.controller.transaction_controller import transaction_bp

basic_auth = BasicAuth()


def create_app(config_object=Config):
  app = Flask(__name__)
  CORS(app)

  app.config.from_object(config_object)

  configure_logging(app)

  Swagger(
    app,
    config=app.config["SWAGGER_CONFIG"],
    template=app.config["SWAGGER_TEMPLATE"],
  )

  db.init_app(app)
  basic_auth.init_app(app)

  register_blueprints(app)
  register_error_handlers(app)

  @app.route("/")
  def home():
    """
    MAIN PAGE
    ---
    responses:
      200:
        description: Returns a message about the service status
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Flask app is running with config from app.yml!
    """
    app.logger.debug("Health check endpoint hit.")
    return {"message": "Flask app is running with config from app.yml!"}

  basic_auth.exempt(home)

  return app


def configure_logging(app):
  logging.basicConfig(level=app.config["LOG_LEVEL"])
  gunicorn_logger = logging.getLogger("gunicorn.error")
  if gunicorn_logger.handlers:
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
  else:
    handler = logging.StreamHandler()
    handler.setFormatter(
      logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    handler.setLevel(app.config["LOG_LEVEL"])
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config["LOG_LEVEL"])
  app.logger.info("Gunicorn-ready Flask application configured.")


def register_blueprints(app):
  app.register_blueprint(customer_bp, url_prefix="/api")
  app.register_blueprint(account_bp, url_prefix="/api")
  app.register_blueprint(transaction_bp, url_prefix="/api")
  app.register_blueprint(card_bp, url_prefix="/api")
  app.register_blueprint(bankdetail_bp, url_prefix="/api")
  app.register_blueprint(customeraddress_bp, url_prefix="/api")
  app.register_blueprint(customeraccount_bp, url_prefix="/api")
  app.register_blueprint(stat_bp, url_prefix="/api")
  app.register_blueprint(split_accounts_bp, url_prefix="/api")


def register_error_handlers(app):
  @app.errorhandler(404)
  def not_found_error(error):
    app.logger.warning("404 encountered: %s", error)
    return {"message": "Resource not found"}, 404

  @app.errorhandler(500)
  def internal_error(error):
    db.session.rollback()
    app.logger.exception("500 encountered: %s", error)
    return {"message": "Internal server error"}, 500


app = create_app()


if __name__ == "__main__":
  app.logger.info("Starting Flask development server; use 'make run' for Gunicorn.")
  app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
