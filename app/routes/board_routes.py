from flask import request, jsonify, abort
from flask_classful import FlaskView, route

from datetime import datetime

from app.project_board_base import ProjectBoardBase
from app.models.user_model import UserRecord
from app.models.team_model import TeamRecord
from app.models.board_model import BoardRecord, BoardStatus
from app.models.task_model import TaskRecord, TaskStatus
from app import db

class BoardRoutes(FlaskView, ProjectBoardBase):
    """Routes implementation for board. Extends ProjectBoardBase.
    """
    def _get_user_by_id(self, user_id):
        user = UserRecord.query.filter_by(id=user_id).first_or_404(description=f"There is no user with id={user_id}")
        return user
    
    def _get_team_by_id(self, team_id):
        team = TeamRecord.query.filter_by(id=team_id).first_or_404(description=f"There is no team with id={team_id}")
        return team

    def _get_board_by_id(self, board_id):
        board = BoardRecord.query.filter_by(id=board_id).first_or_404(description=f"There is no board with id={board_id}")
        return board

    @route('/', methods=['POST'])
    def create_board(self):
        req = request.get_json()
        if not req or not all(item in req for item in ['team_id', 'name', 'description']):
            abort(400, description="Incorrect request body")
        team = self._get_team_by_id(req['team_id'])
        name = req['name']
        for board in team.boards:
            if board.name == name:
                return "Board with same name already exists in this team!"
        creation_time = datetime.now()
        id = int(creation_time.timestamp())
        new_board = BoardRecord(
            name=name,
            description=req['description'],
            team=team,
            creation_time=creation_time,
            id=id
        )
        team.boards.append(new_board)
        try:
            db.session.add(new_board)
            db.session.commit()
        except:
            abort(500, description="Error while adding board to DB")
        return jsonify({"id":id})
    
    @route('/close', methods=['POST'])
    def close_board(self) -> str:
        req = request.get_json()
        board = self._get_board_by_id(req['id'])
        for task in board.tasks:
            if task.task_status != TaskStatus.COMPLETE:
                return "There are incomplete tasks on this board!"
        board.board_status = BoardStatus.CLOSED
        board.end_time = datetime.now()
        try:
            db.session.commit()
        except:
            abort(500, "Error while updating DB")
        return "201"
    
    @route('/add_task', methods=['POST'])
    def add_task(self) -> str:
        req = request.get_json()
        if not req or not all(item in req for item in ['id', 'user_id', 'title', 'description']):
            abort(400, description="Incorrect request body")
        board = self._get_board_by_id(req['id'])
        user = self._get_user_by_id(req['user_id'])
        if user not in board.team.users:
            return "User is not a part of this team!"
        title = req['title']
        for task in board.tasks:
            if task.title == title:
                return "Task with same title already exists!"
        creation_time = datetime.now()
        id = int(creation_time.timestamp())
        new_task = TaskRecord(
            id=id,
            title=req['title'],
            description=req['description'],
            creation_time=creation_time,
            user=user,
            board=board
        )
        board.tasks.append(new_task)
        user.tasks.append(new_task)
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            abort(500, description="Error while adding task to DB")
        return jsonify({'id':id})
    
    @route('/update_task', methods=['POST'])
    def update_task_status(self):
        req = request.get_json()
        id = req['id']
        task = TaskRecord.query.filter_by(id=id).first_or_404(description=f"There is no task with id={id}")
        status = req['status']
        if status=='OPEN':
            task.task_status = TaskStatus.OPEN
        elif status=='IN_PROGRESS':
            task.task_status = TaskStatus.IN_PROGRESS
        elif status=='COMPLETE':
            task.task_status = TaskStatus.COMPLETE
        else:
            abort(400, description="Incorrect status")
        try:
            db.session.commit()
        except:
            abort(500, description="Error while updating DB")
        return "201"
    
    @route('/list', methods=['POST'])
    def list_boards(self) -> str:
        '''Lists boards assigned to a team
        '''
        req = request.get_json()
        team = self._get_team_by_id(req['id'])
        return jsonify([board.list_board() for board in team.boards])
    
    @route('/export', methods=['POST'])
    def export_board(self) -> str:
        req = request.get_json()
        board = self._get_board_by_id(req['id'])
        file = board.export_to_file()
        return jsonify({"out_file": file})
        

