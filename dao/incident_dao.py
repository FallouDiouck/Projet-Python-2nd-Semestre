from dao.base_dao import BaseDAO
from models.incident import Incident
from database.connexion import DatabaseConnection
class IncidentDAO(BaseDAO):
    def __init__(self, connexion):
        super().__init__(connexion)

    def ajout_Incident(self, incident: Incident):
        ## reference a la classe et l'objet
        try:
            db = DatabaseConnection()
            if db.connexion():
              db.execute("""
                INSERT INTO incident (titre, description, priorite, statut, date_creation, utilisateur_id)
                VALUES (%s, %s, %s, %s, NOW(), %s)
            """, (incident.titre, incident.description, incident.priorite,
                  incident.statut, incident.utilisateur_id))
        except Exception as e:
            self.connexion.rollback()
            print("Erreur de creation incident:", e)

    def Modifier_Statut(self, incident_id, nouveau_statut):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute("""
                UPDATE incident SET statut=%s WHERE id=%s
            """, (nouveau_statut, incident_id))
            self.connexion.cursor()
        except Exception as e:
            self.connexion.rollback()
            print("Erreur modif statut:", e)

    def recup_user(self, utilisateur_id):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute("SELECT * FROM incident WHERE utilisateur_id=%s", (utilisateur_id,))
            return db.fetchall()
        except Exception as e:
            print("Erreur de recuperation de l'utulisateur:", e)
            return []

    def filtrer_par_statut(self, utilisateur_id, statut):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute("SELECT * FROM incident WHERE utilisateur_id=%s AND statut=%s",
                           (utilisateur_id, statut))
            return db.fetchall()
        except Exception as e:
            print("Erreur de filtre par statut:", e)
            return []

    def filtrer_par_priorite(self, utilisateur_id, priorite):
        try:
            db = DatabaseConnection()
            if db.connexion() :
             db.execute("SELECT * FROM incident WHERE utilisateur_id=%s AND priorite=%s",
                           (utilisateur_id, priorite))
            return db.fetchall()
        except Exception as e:
            print("Erreur de filtre par priorite:", e)
            return []

    def get_ouvert_enCours(self):
        try:
            db = DatabaseConnection()
            if db.connexion():
               db.execute("""
                SELECT * FROM incident 
                WHERE statut IN ('OUVERT', 'EN_COURS')
            """)
            return db.fetchall()
        except Exception as e:
            print("Erreur lors de la récupération des incidents ouverts/en cours:", e)
            return []

    def recup_technicien(self, technicien_id):
        try:
            db = DatabaseConnection()
            if db.connexion():
             db = self.connexion.cursor()
             db.execute("""
                SELECT i.* 
                FROM incident i
                JOIN intervention inter ON i.id = inter.incident_id
                WHERE inter.technicien_id = %s
            """, (technicien_id,))
            return db.fetchall()
        except Exception as e:
            print("Erreur récupération incidents par technicien:", e)
            return []
        #### gestion des statistiques

    def statistiques(self):
        stats = {}
        try:
            db = DatabaseConnection()
            if db.connexion():
             db.execute("SELECT statut, COUNT(*) FROM incident GROUP BY statut")
             stats["par_statut"] = cursor.fetchall()

             # 2. Nombre d’incidents par priorité
             db.execute("SELECT priorite, COUNT(*) FROM incident GROUP BY priorite")
             stats["par_priorite"] = db.fetchall()

            # 3. Temps moyen de résolution (en heures)
            db.execute("""
                SELECT AVG(EXTRACT(EPOCH FROM (inter.date_intervention - inc.date_creation))/3600)
                FROM incident inc
                JOIN intervention inter ON inc.id = inter.incident_id
                WHERE inc.statut='RESOLU' OR inc.statut='FERME'
            """)
            stats["temps_moyen_resolution_h"] = db.fetchone()[0]

            # 4. Top 3 techniciens les plus actifs (nombre d’interventions)
            db.execute("""
                SELECT technicien_id, COUNT(*) as nb_interventions
                FROM intervention
                GROUP BY technicien_id
                ORDER BY nb_interventions DESC
                LIMIT 3
            """)
            stats["top_techniciens"] = db.fetchall()

            # 5. Pour chaque technicien : nombre d’incidents traités et temps moyen par incident
            db.execute("""
                SELECT inter.technicien_id,
                       COUNT(DISTINCT inter.incident_id) as nb_incidents,
                       AVG(inter.duree_minutes) as duree_moyenne
                FROM intervention inter
                GROUP BY inter.technicien_id
            """)
            stats["techniciens_details"] = db.fetchall()

            # 6. Taux de résolution < 48h
            db.execute("""
                SELECT COUNT(*) FILTER (WHERE EXTRACT(EPOCH FROM (inter.date_intervention - inc.date_creation)) <= 172800),
                       COUNT(*)
                FROM incident inc
                JOIN intervention inter ON inc.id = inter.incident_id
                WHERE inc.statut='RESOLU' OR inc.statut='FERME'
            """)
            resolue_48h, total_resolue = db.fetchone()
            stats["taux_resolution_48h"] = (resolue_48h / total_resolue * 100) if total_resolue > 0 else 0

            return stats

        except Exception as e:
            print("Erreur lors du calcul des statistiques:", e)
            return {}


