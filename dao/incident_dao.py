from dao.base_dao import BaseDAO
from models.incident import Incident

class IncidentDAO(BaseDAO):
    def __init__(self, connexion):
        super().__init__(connexion)

    def ajout_Incident(self, incident: Incident):
        ## reference a la classe et l'objet
        try:
            cursor = self.connexion.cursor()
            cursor.execute("""
                INSERT INTO incident (titre, description, priorite, statut, date_creation, utilisateur_id)
                VALUES (%s, %s, %s, %s, NOW(), %s)
            """, (incident.titre, incident.description, incident.priorite,
                  incident.statut, incident.utilisateur_id))
            self.connexion.commit()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur de creation incident:", e)

    def Modifier_Statut(self, incident_id, nouveau_statut):
        try:
            cursor = self.connexion.cursor()
            cursor.execute("""
                UPDATE incident SET statut=%s WHERE id=%s
            """, (nouveau_statut, incident_id))
            self.connexion.commit()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur modif statut:", e)

    def recup_user(self, utilisateur_id):
        try:
            cursor = self.connexion.cursor()
            cursor.execute("SELECT * FROM incident WHERE utilisateur_id=%s", (utilisateur_id,))
            return cursor.fetchall()
        except Exception as e:
            print("Erreur de recuperation de l'utulisateur:", e)
            return []

    def filtrer_par_statut(self, utilisateur_id, statut):
        try:
            cursor = self.connexion.cursor()
            cursor.execute("SELECT * FROM incident WHERE utilisateur_id=%s AND statut=%s",
                           (utilisateur_id, statut))
            return cursor.fetchall()
        except Exception as e:
            print("Erreur de filtre par statut:", e)
            return []

    def filtrer_par_priorite(self, utilisateur_id, priorite):
        try:
            cursor = self.connexion.cursor()
            cursor.execute("SELECT * FROM incident WHERE utilisateur_id=%s AND priorite=%s",
                           (utilisateur_id, priorite))
            return cursor.fetchall()
        except Exception as e:
            print("Erreur de filtre par priorite:", e)
            return []
