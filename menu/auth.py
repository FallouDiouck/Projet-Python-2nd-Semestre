from dao.utulisateur_dao import UtilisateurDAO

def authentification():
    print("=== Connexion ===")
    login = input("Login: ")
    password = input("Mot de passe: ")

    dao = UtilisateurDAO()
    user = dao.authentifier(login, password)

    if user:
        print(f"Bienvenue {user.prenom} {user.nom} ({user.role})")
        return user
    else:
        print("Identifiants incorrects")
        return None