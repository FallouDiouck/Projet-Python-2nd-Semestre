from datetime import date


class Utilisateur:
    def __init__(self, id=None, login="", password="", nom="", prenom="",
                 email="", role="UTILISATEUR", service="",
                 date_creation=None):
        self.id = id
        self.login = login
        self.password = password
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.role = role
        self.service = service
        self.date_creation = date_creation or date.today()

    def __str__(self):
        return (f"ID : {self.id} | "
                f"{self.nom} {self.prenom} | "
                f"Login : {self.login} | "
                f"Role : {self.role}")