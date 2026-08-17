from dao.utulisateur_dao import UtilisateurDAO
from dao.incident_dao import IncidentDAO
from dao.intervention_dao import InterventionDAO
from models.incident import Incident
from database.connexion import DatabaseConnection
from models.intervention import Intervention
from models.utilisateur import Utilisateur

def menu_utilisateur(user):


    connexion = DatabaseConnection().connexion
    # Instancier le DAO avec la connexion
    dao_incident = IncidentDAO(connexion)
    while True:
        print("\n=== Menu Utilisateur ===")
        print("1. Créer un incident")
        print("2. Lister mes incidents")
        print("3. Filtrer mes incidents par statut")
        print("4. Filtrer mes incidents par priorité")
        print("0. Déconnexion")

        choix = input("Votre choix: ")
        if choix == "1":
            # Saisie des informations
            titre = input("Titre: ")
            desc = input("Description: ")
            priorite = input("Priorité (BASSE, MOYENNE, HAUTE, CRITIQUE): ")

            # Création de l’objet Incident
            incident = Incident(
                titre=titre,
                description=desc,
                priorite=priorite,
                statut="OUVERT",  # statut initial obligatoire
                utilisateur_id=user.id
            )

            # Appel DAO
            dao_incident.ajout_Incident(incident) # car ajout incident attend un objet
        elif choix == "2":
            incidents = dao_incident.recup_user(user.id)
            for inc in incidents:
                print(inc)
        elif choix == "3":
            statut = input("Statut: ")
            incidents = dao_incident.filtrer_par_statut(user.id, statut)
            for inc in incidents:
                print(inc)
        elif choix == "4":
            priorite = input("Priorité: ")
            incidents = dao_incident.filtrer_par_priorite(user.id, priorite)
            for inc in incidents:
                print(inc)
        elif choix == "0":
            break

def menu_technicien(user):
    connexion = DatabaseConnection().connexion
    dao_incident = IncidentDAO(connexion)
    dao_intervention = InterventionDAO(connexion)

    while True:
        print("\n=== Menu Technicien ===")
        print("1. Consulter incidents ouverts/en cours")
        print("2. Prendre en charge un incident")
        print("3. Ajouter une intervention")
        print("4. Résoudre un incident")
        print("5. Fermer un incident")
        print("6. Historique de mes incidents")
        print("0. Déconnexion")

        choix = input("Votre choix: ")

        if choix == "1":
            incidents = dao_incident.get_ouvert_enCours()
            for inc in incidents:
                print(inc)

        elif choix == "2":
            id_incident = int(input("ID incident: "))
            dao_incident.Modifier_Statut(id_incident, "EN_COURS")

        elif choix == "3":
            id_incident = int(input("ID incident: "))
            commentaire = input("Commentaire: ")
            duree = int(input("Durée (minutes): "))

            intervention = Intervention(
                commentaire=commentaire,
                duree_minutes=duree,
                incident_id=id_incident,
                technicien_id=user.id
            )
            dao_intervention.ajout_interv(intervention)

        elif choix == "4":
            id_incident = int(input("ID incident: "))
            dao_incident.Modifier_Statut(id_incident, "RESOLU")

        elif choix == "5":
            id_incident = int(input("ID incident: "))
            dao_incident.Modifier_Statut(id_incident, "FERME")

        elif choix == "6":
            incidents = dao_incident.recup_technicien(user.id)
            for inc in incidents:
                print(inc)

        elif choix == "0":
            break


def menu_admin():
    connexion = DatabaseConnection().connexion
    dao_user = UtilisateurDAO(connexion)
    dao_incident = IncidentDAO(connexion)
    while True:
        print("\n=== Menu Admin ===")
        print("1. Gestion des utilisateurs (CRUD)")
        print("2. Consulter tous les incidents")
        print("3. Statistiques")
        print("0. Déconnexion")
        choix = input("Votre choix: ")
        if choix == "1":
            print("1 Ajouter un utilisateur")
            print("2 Modifier un utilisateur")
            print("3 Supprimer un utilisateur")
            print("4 Retour")
            ch = input("Faite votre choix")
            if ch == "1":
                nom = input("Nom : ")
                prenom = ("Prenom : ")
                login = input("Login : ")
                email = input("Email : ")
                password = input("Passeword : ")
                service = input("Service : ")

                user = Utilisateur(
                    login=login,
                    password=password,
                    nom=nom,
                    prenom=prenom,
                    email=email,
                    role="Utilisateur",
                    service=service
                    )
                dao_user.ajouterUser(user)
            elif ch == "2":
                id = input("Saisir ID : ")
                user = dao_user.get_by_id("utilisateur", id)
                user.nom = input("Nouveau nom : ") or user.nom
                user.prenom = input("Nouveau prenom : ") or user.prenom
                user.password = input(" : ") or user.password
                user.login = input("Login : ") or user.login
                user.role = input("Role : ") or user.role
                user.service = input("Service : ") or user.service

                dao_user.Modification(user)
            elif ch == "3":
                id = input("Saisir ID : ")
                user = dao_user.get_by_id("utilisateur", id)
                if user:
                    dao_user.delete_by_id("utilisateur", id)
            elif ch == "4":
                break
        elif choix == "2":
            incidents = dao_incident.get_all("incident")
            for inc in incidents:
                print(inc)
        elif choix == "3":
            stats = dao_incident.statistiques()
            print(stats)
        elif choix == "0":
            break
