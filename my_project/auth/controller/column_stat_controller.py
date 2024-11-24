from flask import Blueprint, request, jsonify
from my_project.auth.service.column_stat_service import ColumnStatService

stat_bp = Blueprint('stats', __name__)

@stat_bp.route('/column_stat', methods=['GET'])
def get_column_stat():
    try:
        table_name = request.args.get('table_name')
        column_name = request.args.get('column_name')
        stat_type = request.args.get('stat_type')

        if not table_name or not column_name or not stat_type:
            return jsonify({"message": "Parameters 'table_name', 'column_name', and 'stat_type' are required."}), 400

        result = ColumnStatService.get_column_stat(table_name, column_name, stat_type)

        if result is not None:
            return jsonify({"result": result}), 200
        return jsonify({"message": "No result returned from procedure."}), 404

    except Exception as e:
        return jsonify({"message": str(e)}), 400
