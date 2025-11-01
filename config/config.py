import boto3
import json
import os


def get_secret(secret_name, region_name="eu-north-1"):
    """Отримати секрет з AWS Secrets Manager"""
    client = boto3.client("secretsmanager", region_name=region_name)

    response = client.get_secret_value(SecretId=secret_name)

    if "SecretString" in response:
        secret = response["SecretString"]
        return json.loads(secret)
    else:
        return json.loads(response["SecretBinary"])


class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")

    try:
        secret = get_secret("prod/mysql/beta")

        DB_USER = secret["username"]
        DB_PASSWORD = secret["password"]
        DB_HOST = secret["host"]
        DB_PORT = secret["port"]
        DB_NAME = os.getenv("DB_NAME", "private_bank_lab5")

        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    except Exception as e:
        print("⚠️ Не вдалося отримати секрет з AWS:", e)
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://root:password@localhost:3306/private_bank_lab5"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME", "admin")
    BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD", "password")
    BASIC_AUTH_FORCE = True
    BASIC_AUTH_REALM = os.getenv("BASIC_AUTH_REALM", "Protected API")
    SWAGGER = {
        "title": os.getenv("SWAGGER_TITLE", "Private Bank API"),
        "uiversion": int(os.getenv("SWAGGER_UI_VERSION", "3")),
    }
    SWAGGER_TEMPLATE = {
        "swagger": os.getenv("SWAGGER_SPEC_VERSION", "2.0"),
        "info": {
            "title": os.getenv("SWAGGER_TITLE", "Private Bank API"),
            "description": os.getenv(
                "SWAGGER_DESCRIPTION",
                "API documentation for the banking service. Use the Authorize button and enter the BASIC_AUTH_USERNAME/BASIC_AUTH_PASSWORD to try secured endpoints.",
            ),
            "version": os.getenv("SWAGGER_VERSION", "1.0.0"),
        },
        "host": os.getenv("SWAGGER_HOST", "localhost:8000"),
        "basePath": os.getenv("SWAGGER_BASE_PATH", "/api"),
        "schemes": [os.getenv("SWAGGER_SCHEME", "http")],
        "securityDefinitions": {
            "basicAuth": {
                "type": "basic",
                "description": "Standard HTTP Basic authentication."
            }
        },
        "security": [{"basicAuth": []}],
    }
    SWAGGER_CONFIG = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route": os.getenv("SWAGGER_SPEC_ROUTE", "/apispec_1.json"),
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": os.getenv("SWAGGER_UI_ROUTE", "/apidocs/"),
    }
    GUNICORN_CMD_ARGS = os.getenv(
        "GUNICORN_CMD_ARGS", "--workers 3 --bind 0.0.0.0:8000 --timeout 120"
    )
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")