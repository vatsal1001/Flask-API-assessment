from . import db, users_teams
from datetime import datetime

class UserRecord(db.Model):
    __tablename__ = "user"
    name = db.Column(db.String(64), unique=True)
    display_name = db.Column(db.String(64), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, default=datetime.now)
    admin_of = db.relationship("TeamRecord", backref="admin")
    teams = db.relationship("TeamRecord", secondary=users_teams, backref="users")
    tasks = db.relationship("TaskRecord", backref="user")

    def __repr__(self):
        return f"<User: {self.name}\t{self.display_name}\t{self.id}\t{self.creation_time}>"
    
    def get_description(self):
        admins = [team.name for team in self.admin_of]
        teams = [team.name for team in self.teams]
        tasks = [task.title for task in self.tasks]
        return f"Name={self.name}, admins={admins}, teams={teams}, tasks={tasks}"

    def list_user(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "creation_time": self.creation_time
        }
    
    def describe(self):
        return {
            "name": self.name,
            "description": self.get_description(),
            "creation_time": self.creation_time
        }
    
    def list_users_for_team(self):
        return {
            "id":self.id,
            "name":self.name,
            "display_name":self.display_name
        }