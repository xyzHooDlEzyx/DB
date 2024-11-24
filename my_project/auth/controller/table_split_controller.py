from flask import Blueprint, jsonify
from my_project.auth.service.table_split_service import SplitAccountsService

split_accounts_bp = Blueprint('split_accounts', __name__)

@split_accounts_bp.route('/split_accounts', methods=['POST'])
def split_accounts():
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
