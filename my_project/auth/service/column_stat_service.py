from extensions import db
from sqlalchemy.sql import text

class ColumnStatService:
    @staticmethod
    def get_column_stat(table_name, column_name, stat_type):
        try:
            if table_name == "Accounts" and column_name == "Balance":
                result = db.session.execute(
                    text("SELECT GetBalanceStat(:stat_type) AS result"),
                    {'stat_type': stat_type}
                ).fetchone()

                if result:
                    return result[0]
                else:
                    return None
            else:
                return None

        except Exception as e:
            raise e
