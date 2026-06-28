from database.connexion import DatabaseConnection


def create_tables():
    """Création des tables utilisateur, incident, intervention"""

    db = DatabaseConnection()

    if not db.connexion():
        print("Connexion échouée")
        return False

    try:
        # ===================== TABLE UTILISATEUR =====================
        sql_utilisateur = """
        CREATE TABLE IF NOT EXISTS utilisateur (
            id INT AUTO_INCREMENT PRIMARY KEY,
            login VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            nom VARCHAR(100) NOT NULL,
            prenom VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            role ENUM('UTILISATEUR', 'TECHNICIEN', 'ADMIN') NOT NULL,
            service VARCHAR(100),
            date_creation DATE DEFAULT (CURRENT_DATE)
        ) ENGINE=InnoDB
        """

        # ===================== TABLE INCIDENT =====================
        sql_incident = """
        CREATE TABLE IF NOT EXISTS incident (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titre VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            priorite ENUM('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE') NOT NULL,
            statut ENUM('OUVERT', 'EN_COURS', 'RESOLU', 'FERME') DEFAULT 'OUVERT',
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            utilisateur_id INT NOT NULL,
            CONSTRAINT fk_utilisateur FOREIGN KEY (utilisateur_id)
                REFERENCES utilisateur(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """

        # ===================== TABLE INTERVENTION =====================
        sql_intervention = """
        CREATE TABLE IF NOT EXISTS intervention (
            id INT AUTO_INCREMENT PRIMARY KEY,
            commentaire TEXT NOT NULL,
            duree_minutes INT DEFAULT 0,
            date_intervention DATETIME DEFAULT CURRENT_TIMESTAMP,
            incident_id INT NOT NULL,
            technicien_id INT NOT NULL,
            CONSTRAINT fk_incident FOREIGN KEY (incident_id)
                REFERENCES incident(id) ON DELETE RESTRICT,
            CONSTRAINT fk_technicien FOREIGN KEY (technicien_id)
                REFERENCES utilisateur(id) ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """

        # ===================== EXECUTION =====================
        tables = [
            ("utilisateur", sql_utilisateur),
            ("incident", sql_incident),
            ("intervention", sql_intervention)
        ]

        for name, sql in tables:
            print(f"→ Création table {name} ...")

            if not db.execute(sql):
                raise Exception(f"Erreur création table {name}")

        db.commit()
        print("\nToutes les tables ont été créées avec succès !")
        return True

    except Exception as e:
        print(f"Erreur globale : {e}")
        db.rollback()
        return False

    finally:
        db.disconnect()


if __name__ == "__main__":
    create_tables()