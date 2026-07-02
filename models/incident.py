from datetime import datetime


class Incident:

    def __init__(self, id=None, titre="", description="", priorite="",
                 statut="OUVERT", date_creation=None, utilisateur_id=None):

        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut
        self.date_creation = date_creation if date_creation else datetime.now()
        self.utilisateur_id = utilisateur_id

    def __str__(self):
        return (f"Incident {self.id} | "
                f"{self.titre} | "
                f"Priorité : {self.priorite} | "
                f"Statut : {self.statut}")