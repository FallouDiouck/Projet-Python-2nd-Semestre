from dao.base_dao import BaseDAO
from models.utilisateur import Utilisateur
from database.connexion import DatabaseConnection

class UtilisateurDAO(BaseDAO):
    def __init__(self, connexion):
        super().__init__(connexion)
            ###################### suppresion et recherche par id gerer par la classe abstraite BaseDao
    def ajouterUser(self, utilisateur):
               ## db = DatabaseConnection()  # pas besoin d'instancier gerer par BaseDao

                sql = """
            INSERT INTO utilisateur (login, password, nom, prenom, email, role, service, date_creation)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
                params = (
                    utilisateur.login,
                    utilisateur.password,
                    utilisateur.nom,
                    utilisateur.prenom,
                    utilisateur.email,
                    utilisateur.role,
                    utilisateur.service
                )

                db = DatabaseConnection()
                try:
                    if db.connexion():
                     db.execute(sql, params)
                     db.commit()
                    return True
                except Exception as e:
                  db.rollback()
                  print("Erreur lors de l'ajout:", e)
                return False


    def Modification(self, utilisateur: Utilisateur):
        db = DatabaseConnection()
        try:
            if db.connexion():
             db.execute("""
                UPDATE utilisateur SET password=%s, nom=%s, prenom=%s, email=%s, role=%s, service=%s
                WHERE id=%s
               """, (utilisateur.password, utilisateur.nom, utilisateur.prenom,
                  utilisateur.email, utilisateur.role, utilisateur.service, utilisateur.id))
             db.commit()
        except Exception as e:
            db.rollback()
            print("Erreur update utilisateur:", e)

    ##########" gerer l'authentification

    def authentifier(self, login, password):
              db = DatabaseConnection()
              if not db.connexion():
                  return None
              sql = """
            SELECT * FROM utilisateur
            WHERE login= %s AND password=%s
            """
              params = (login, password)
              db.execute(sql, params)
              ligne = db.fetchone()
              db.disconnect()
              if ligne:
                  return Utilisateur(
                      id=ligne[0],
                      login=ligne[1],
                      password=ligne[2],
                      nom=ligne[3],
                      prenom=ligne[4],
                      email=ligne[5],
                      role=ligne[6],
                      service=ligne[7],
                      date_creation=ligne[8]
                  )
              return None




