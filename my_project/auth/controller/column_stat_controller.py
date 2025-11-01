from flask import Blueprint, jsonify, request

from my_project.auth.service.column_stat_service import ColumnStatService

stat_bp = Blueprint('stats', __name__)


@stat_bp.route('/column_stat', methods=['GET'])
def get_column_stat():
    """
    Get statistics for a specific column in a table
    ---
    tags:
      - ColumnStats
    parameters:
      - name: table_name
        in: query
        required: true
        schema:
          type: string
        description: Name of the table
      - name: column_name
        in: query
        required: true
        schema:
          type: string
        description: Name of the column
      - name: stat_type
        in: query
        required: true
        schema:
          type: string
        description: Type of statistic (e.g., min, max, avg, sum)
    responses:
      200:
        description: Returns the requested statistic
        content:
          application/json:
            schema:
              type: object
              properties:
                result:
                  type: number
                  example: 123.45
      400:
        description: Missing or invalid parameters
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Parameters 'table_name', 'column_name', and 'stat_type' are required.
      404:
        description: No result returned from procedure
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: No result returned from procedure.
    """
    table_name = request.args.get('table_name')
    column_name = request.args.get('column_name')
    stat_type = request.args.get('stat_type')

    if not table_name or not column_name or not stat_type:
        return jsonify({"message": "Parameters 'table_name', 'column_name', and 'stat_type' are required."}), 400

    try:
        result = ColumnStatService.get_column_stat(table_name, column_name, stat_type)
    except Exception as exc:
        return jsonify({"message": str(exc)}), 400

    if result is not None:
        return jsonify({"result": result}), 200

    return jsonify({"message": "No result returned from procedure."}), 404
