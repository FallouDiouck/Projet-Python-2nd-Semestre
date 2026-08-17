### Authentification ( user / technicien / admin)

from dao.base_dao import BaseDAO
from models.intervention import Intervention

class InterventionDAO(BaseDAO):
    def __init__(self, connexion):
        super().__init__(connexion)

    def ajout_interv(self, intervention: Intervention):
        try:
            db = DatabaseConnection()
            if db.connexion():
              db.execute("""
                INSERT INTO intervention (commentaire, duree_minutes, date_intervention, incident_id, technicien_id)
                VALUES (%s, %s, NOW(), %s, %s)
            """, (intervention.commentaire, intervention.duree_minutes,
                  intervention.incident_id, intervention.technicien_id))
            self.connexion.commit()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur create intervention:", e)

    def Recup_id_incident(self, incident_id):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute("SELECT * FROM intervention WHERE incident_id=%s", (incident_id,))
            return db.fetchall()
        except Exception as e:
            print("Erreur de recuperation de l'incident:", e)
            return []

    def Recup_par_technicien(self, technicien_id):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute("SELECT * FROM intervention WHERE technicien_id=%s", (technicien_id,))
            return db.fetchall()
        except Exception as e:
            print("Erreur get_by_technicien:", e)
            return []
