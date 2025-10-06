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
