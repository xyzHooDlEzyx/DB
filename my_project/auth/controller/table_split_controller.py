from flask import Blueprint, jsonify
from my_project.auth.service.table_split_service import SplitAccountsService

split_accounts_bp = Blueprint('split_accounts', __name__)

@split_accounts_bp.route('/split_accounts', methods=['POST'])
def split_accounts():
    """
    Split accounts into separate tables
    ---
    tags:
      - TableSplit
    responses:
      201:
        description: Tables created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: Tables created successfully
            tables:
              type: array
              items:
                type: string
              example: ["accounts_1", "accounts_2"]
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            message:
              type: string
              example: Error message
    """
    try:
        tables = SplitAccountsService.split_accounts()
        return jsonify({
            "message": "Tables created successfully",
            "tables": tables
        }), 201
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
