from dao.base_dao import BaseDAO
from models import Utilisateur
from database.connexion import DatabaseConnection
from models.Utilisateur import Utulisateur

class UtilisateurDAO(BaseDAO):
            ######################
    def ajouterUser(self, utilisateur):
                db = DatabaseConnection()  # instance
                if not db.connexion:
                    print("Pas de connexion")
                    return False

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

                try:
                    ok = db.execute(sql, params)
                    if ok:
                        db.commit()
                    return ok
                except Exception as e:
                    db.rollback()
                    print("Erreur lors de l'ajout:", e)
                    return False
                finally:
                    db.disconnect()

    def RechercherparLogin(self, login):
        try:
            cursor = self.connexion.cursor()
            cursor.execute("SELECT * FROM utilisateur WHERE login=%s", (login,))
            row = cursor.fetchone()
            if row:
                return Utilisateur(*row[1:], id=row[0], date_creation=row[-1])
            return None
        except Exception as e:
            print("Erreur RechercherparLogin:", e)
            return None

    def Modification(self, utilisateur: Utulisateur):
        try:
            cursor = self.connexion.cursor()
            cursor.execute("""
                UPDATE utilisateur SET password=%s, nom=%s, prenom=%s, email=%s, role=%s, service=%s
                WHERE id=%s
            """, (utilisateur.password, utilisateur.nom, utilisateur.prenom,
                  utilisateur.email, utilisateur.role, utilisateur.service, utilisateur.id))
            self.connexion.commit()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur update utilisateur:", e)