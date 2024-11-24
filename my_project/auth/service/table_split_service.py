from extensions import db

class SplitAccountsService:
    @staticmethod
    def split_accounts():

        raw_connection = None
        try:
            raw_connection = db.engine.raw_connection()
            cursor = raw_connection.cursor()

            cursor.callproc("SplitAccountsIntoRandomTables")

            print("Checking stored results...")
            for result in cursor.stored_results():
                print(f"Result: {result}")

                row = result.fetchone()
                if row:
                    tables = {"Table1": row[0], "Table2": row[1]}
                    print(f"Result fetched: {tables}")

                    raw_connection.commit()
                    return tables

            raise RuntimeError("Procedure returned no results.")

        except Exception as e:
            raise RuntimeError(f"Error while executing procedure: {str(e)}")

        finally:
            if raw_connection:
                raw_connection.close()
