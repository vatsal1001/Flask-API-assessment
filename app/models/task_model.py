from . import db
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    OPEN = 0
    IN_PROGRESS = 1
    COMPLETE = 2

class TaskRecord(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(128))
    creation_time = db.Column(db.DateTime, default=datetime.now)
    task_status = db.Column(db.Enum(TaskStatus), default=TaskStatus.OPEN)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))

    def __repr__(self):
        return f"<Task {self.id}\t{self.title}\t{self.task_status}>"
