
from menu.auth import authentification
from menu.interface import menu_utilisateur, menu_technicien, menu_admin

def main():
    user = authentification()
    if not user:
        return

    if user.role == "UTILISATEUR":
        menu_utilisateur(user)
    elif user.role == "TECHNICIEN":
        menu_technicien(user)
    elif user.role == "ADMIN":
        menu_admin()

main()
