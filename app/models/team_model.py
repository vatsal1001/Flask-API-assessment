from . import db
from datetime import datetime

class TeamRecord(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    creation_time = db.Column(db.DateTime, default=datetime.now)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    boards = db.relationship("BoardRecord", backref="team")

    def __repr__(self):
        return f"<Team {self.name}\t{self.creation_time}"
    
    def list_team(self):
        return {
            "name": self.name,
            "description": self.description,
            "creation_time": self.creation_time,
            "admin": self.admin_id
        }
    
    def list_teams_for_user(self):
        return {
            "name": self.name,
            "description": self.description,
            "creation_time": self.creation_time
        }