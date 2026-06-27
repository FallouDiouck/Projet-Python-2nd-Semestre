import mysql.connector
from database.config import TYPE_BD, MYSQL

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance

    def connexion(self):
        try:
            if TYPE_BD == "mysql":
                self.connection = mysql.connector.connect(
                    host=MYSQL["host"],
                    port=MYSQL["port"],
                    database=MYSQL["database"],
                    user=MYSQL["user"],
                    password=MYSQL["password"],
                )
                print("Connexion réussie à MySQL")
            else:
                print("Type de base de données introuvable")
                return False

            self.cursor = self.connection.cursor()
            return True

        except Exception as e:
            print(f"Erreur de connexion à la base de données : {e}")
            return False

    def disconnect(self):
        # fermer la connexion
        if self.cursor:
            self.cursor.close()

        if self.connection:
            self.connection.close()
            print(f"connexion fermee")


    def commit(self):
        # Valider les modifications
        if self.connexion:
            self.connection.commit()


    def rollback(self):
        # retour ou Annule les modifications
        if self.connexion:
            self.connection.rollback()


    def execute(self, query, params=None):
        # execute une requete sql
        try:
            self.cursor.execute(query, params or ())
            return True
        except Exception as e:
            print(f"Erreur de requette SQL:{e}")
            return False


    def fetchall(self):
        # recupere tout les resultats
        return self.connection.fetchall()


    def fetchone(self):
        # recupère un seul résultat
        return self.connection.fetchone()