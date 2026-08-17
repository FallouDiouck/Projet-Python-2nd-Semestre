from database.connexion import DatabaseConnection


def insert_test_data():
    """Insertion de données de test"""

    db = DatabaseConnection()
    if not db.connexion():
        print("Connexion échouée")
        return False

    try:
        # ===================== UTILISATEURS =====================
        utilisateurs = [
            # (login, password, nom, prenom, email, role, service)
            ("admin", "admin123", "Diallo", "Mamadou", "admin@isi.sn", "ADMIN", "Informatique"),
            ("tech1", "tech123", "Ndiaye", "Ibrahima", "tech1@isi.sn", "TECHNICIEN", "Informatique"),
            ("tech2", "tech123", "Sow", "Fatou", "tech2@isi.sn", "TECHNICIEN", "Informatique"),
            ("user1", "user123", "Fall", "Moussa", "user1@isi.sn", "UTILISATEUR", "Comptabilité"),
            ("user2", "user123", "Ba", "Aminata", "user2@isi.sn", "UTILISATEUR", "RH"),
            ("user3", "user123", "Diop", "Omar", "user3@isi.sn", "UTILISATEUR", "Marketing"),
        ]

        sql_utilisateur = """
        INSERT INTO utilisateur(login, password, nom, prenom, email, role, service)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """

        print("Insertion des utilisateurs")
        for u in utilisateurs:
            db.execute(sql_utilisateur, u)
        db.commit()
        print("Utilisateurs insérés !")

        # ===================== INCIDENTS =====================
        incidents = [
            # (titre, description, priorite, statut, utilisateur_id)
            ("Panne réseau", "Impossible de se connecter à internet", "HAUTE", "OUVERT", 4),
            ("Imprimante HS", "L'imprimante du bureau ne fonctionne plus", "MOYENNE", "EN_COURS", 5),
            ("PC lent", "Mon ordinateur est très lent depuis ce matin", "BASSE", "OUVERT", 6),
            ("Virus détecté", "Alerte antivirus sur mon poste", "CRITIQUE", "EN_COURS", 4),
            ("Email bloqué", "Je ne reçois plus mes emails", "MOYENNE", "RESOLU", 5),
            ("Ecran noir", "Mon écran s'éteint aléatoirement", "HAUTE", "FERME", 6),
        ]

        sql_incident = """
        INSERT INTO incident(titre, description, priorite, statut, utilisateur_id)
        VALUES(%s, %s, %s, %s, %s)
        """

        print("Insertion des incidents")
        for i in incidents:
            db.execute(sql_incident, i)
        db.commit()
        print("Incidents insérés !")

        # ===================== INTERVENTIONS =====================
        interventions = [
            # (commentaire, duree_minutes, incident_id, technicien_id)
            ("Vérification du câble réseau et redémarrage du routeur", 30, 2, 2),
            ("Analyse antivirus complète effectuée", 120, 4, 3),
            ("Nettoyage du système et suppression des fichiers temporaires", 45, 5, 2),
            ("Remplacement de l'écran défectueux", 60, 6, 3),
        ]

        sql_intervention = """
        INSERT INTO intervention(commentaire, duree_minutes, incident_id, technicien_id)
        VALUES(%s, %s, %s, %s)
        """

        print("Insertion des interventions")
        for i in interventions:
            db.execute(sql_intervention, i)
        db.commit()
        print("Interventions insérées !")

        print("\nToutes les données de test ont été insérées avec succès !")
        return True

    except Exception as e:
        print(f"Erreur : {e}")
        db.rollback()
        return False

    finally:
        db.disconnect()


if __name__ == "__main__":
    insert_test_data()