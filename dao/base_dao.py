from database.connexion import DatabaseConnection


class BaseDAO:
    def __init__(self, connexion):
        self.connexion = connexion
      ### INSTANCIATION A LA BD A FAIRE DANS LE MAIN POUR USE LES FONSCTION DU DAO
    ### NOM_TABLE A COMPLETER PAR LA TABLE SUR LA QUELLE ON EXECUTE LES FONCTIONS
    def get_all(self, nom_table):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute(f"SELECT * FROM {nom_table}")
             return db.fetchall()
        except Exception as e:
            print("Erreur get_all:", e)
            return []

    def get_by_id(self, nom_table, id):
        try:
            db = DatabaseConnection()
            db.execute(f"SELECT * FROM {nom_table} WHERE id=%s", (id,))
            return db.fetchone()
        except Exception as e:
            print("Erreur get_by_id:", e)
            return None

    def delete_by_id(self, nom_table, id):
        try:
            db = DatabaseConnection()
            db.execute(f"DELETE FROM {nom_table} WHERE id=%s", (id,))
            self.connexion.commit()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur delete_by_id:", e)
