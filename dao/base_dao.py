class BaseDAO:
    def __init__(self, connexion):
        self.connexion = connexion

    def get_all(self, table_name):
        try:
            cursor = self.connexion.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            return cursor.fetchall()
        except Exception as e:
            print("Erreur get_all:", e)
            return []

    def get_by_id(self, table_name, id):
        try:
            cursor = self.connexion.cursor()
            cursor.execute(f"SELECT * FROM {table_name} WHERE id=%s", (id,))
            return cursor.fetchone()
        except Exception as e:
            print("Erreur get_by_id:", e)
            return None

    def delete_by_id(self, table_name, id):
        try:
            cursor = self.connexion.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE id=%s", (id,))
            self.connexion.commit()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur delete_by_id:", e)
