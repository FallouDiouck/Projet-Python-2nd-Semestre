from datetime import datetime


class Intervention:

    def __init__(self, id=None, commentaire="", duree_minutes=0,
                 date_intervention=None, incident_id=None, technicien_id=None):

        self.id = id
        self.commentaire = commentaire
        self.duree_minutes = duree_minutes
        self.date_intervention = (
            date_intervention if date_intervention else datetime.now()
        )
        self.incident_id = incident_id
        self.technicien_id = technicien_id

    def __str__(self):
        return (f"Intervention {self.id} | "
                f"Durée : {self.duree_minutes} min | "
                f"Incident : {self.incident_id} | "
                f"Technicien : {self.technicien_id}")