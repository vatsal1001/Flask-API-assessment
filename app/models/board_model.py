from app.models.task_model import TaskStatus
from . import db
from datetime import datetime
from enum import Enum

class BoardStatus(Enum):
    OPEN = 0
    CLOSED = 1

class BoardRecord(db.Model):
    __tablename__ = "board"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    creation_time = db.Column(db.DateTime, default=datetime.now)
    end_time = db.Column(db.DateTime)
    board_status = db.Column(db.Enum(BoardStatus), default=BoardStatus.OPEN)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"))
    tasks = db.relationship("TaskRecord", backref="board")

    def __repr__(self):
        return f"<Board {self.id}\t{self.name}\t{self.board_status}>"
    
    def list_board(self):
        return {
            "id":self.id,
            "name":self.name
        }
    
    def export_to_file(self):
        with open(f"out/{self.id}.txt", "w+") as f:
            f.write("\n{0:^64s}\n\n".format(self.name.upper()))
            f.write(f"ID = {self.id}\n")
            f.write(f"Created on {self.creation_time}\n\n")
            f.write(self.description)
            f.write(f"\n\nBelongs to team: {self.team.name}\n")
            f.write(f"Admin: {self.team.admin.name}\n")
            f.write("\n{0:^64s}\n".format("BOARD STATUS: " + self.board_status.name))
            f.write("\n")
            f.write(" OPEN TASKS ".center(32, '-'))
            f.write("\n\n")
            total_tasks = len(self.tasks)
            for task in self.tasks:
                if task.task_status == TaskStatus.OPEN:
                    f.write(f"[ ] {task.title}\n")
                    f.write(f"\t- {task.description}\n")
                    f.write(f"\t- Assigned to: {task.user.name}\n")
            f.write("\n")
            f.write(" IN_PROGRESS TASKS ".center(32, '-'))
            f.write("\n\n")
            for task in self.tasks:
                if task.task_status == TaskStatus.IN_PROGRESS:
                    f.write(f"[o] {task.title}\n")
                    f.write(f"\t- {task.description}\n")
                    f.write(f"\t- Assigned to: {task.user.name}\n")
            f.write("\n")
            f.write(" COMPLETED TASKS ".center(32, '-'))
            f.write("\n\n")
            completed_tasks = 0
            for task in self.tasks:
                if task.task_status == TaskStatus.COMPLETE:
                    completed_tasks += 1
                    f.write(f"[X] {task.title}\n")
                    f.write(f"\t- {task.description}\n")
                    f.write(f"\t- Assigned to: {task.user.name}\n")
            f.write(f"\n{completed_tasks} out of {total_tasks} tasks are completed")
        return f"{self.id}.txt"