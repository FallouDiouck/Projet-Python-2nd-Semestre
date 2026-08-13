from dao.utulisateur_dao import UtilisateurDAO
from database.connexion import DatabaseConnection


def authentification():
    print("=== Connexion ===")
    login = input("Login: ")
    password = input("Mot de passe: ")
    connexion = DatabaseConnection().connexion
    dao = UtilisateurDAO(connexion)
    user = dao.authentifier(login, password)

    if user:
        print(f"Bienvenue {user.prenom} {user.nom} ({user.role})")
        return user
    else:
        print("Identifiants incorrects")
        return None