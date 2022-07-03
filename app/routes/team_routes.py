from flask import request, jsonify, abort
from flask_classful import FlaskView, route

from datetime import datetime
import random

from app.team_base import TeamBase
from app.models.team_model import TeamRecord
from app.models.user_model import UserRecord
from app import db

class TeamRoutes(FlaskView, TeamBase):
    """
    Routes implementation for team. Extends TeamBase class.
    """
    def _get_user_by_id(self, user_id):
        user = UserRecord.query.filter_by(id=user_id).first_or_404(description=f"There is no user with id={user_id}")
        return user
    
    def _get_team_by_id(self, team_id):
        team = TeamRecord.query.filter_by(id=team_id).first_or_404(description=f"There is no team with id={team_id}")
        return team
    
    @route('/', methods=['POST'])
    def create_team(self) -> str:
        req = request.get_json()
        if not req or not all(item in req for item in ["name", "description", "admin"]):
            abort(400, description="Incorrect parameters in request body")
        admin = self._get_user_by_id(req['admin'])
        creation_time = datetime.now()
        id = int(creation_time.timestamp())
        new_team = TeamRecord(
            name=req['name'],
            description=req['description'],
            admin=admin,
            id=id,
            creation_time=creation_time
        )
        new_team.users.append(admin)
        admin.teams.append(new_team)
        try:
            db.session.add(new_team)
            db.session.commit()
        except:
            abort(500, description="Error while adding team to DB")
        return jsonify({"id":id})
    
    @route('/', methods=['GET'])
    def list_teams(self) -> str:
        try:
            teams = TeamRecord.query.all()
            return jsonify([team.list_team() for team in teams])
        except:
            abort(500, description="Error while fetching teams")
    
    @route('/<int:team_id>', methods=['GET'])
    def describe_team_REST(self, team_id):
        team = self._get_team_by_id(team_id)
        return jsonify(team.list_team())
    
    @route('/describe', methods=['POST'])
    def describe_team(self) -> str:
        try:
            req = request.get_json()
            return self.describe_team_REST(req['id'])
        except:
            abort(400, description="Incorrect request parameters")
    
    def _update_team_helper(self, team_id, name, description, admin):
        """Helper function to update database with above parameters
        """
        team = self._get_team_by_id(team_id)
        admin = self._get_user_by_id(admin)
        team.name = name
        team.description = description
        team.admin = admin
        if admin not in team.users:
            team.users.append(admin)
        try:
            db.session.commit()
            return '201'
        except:
            return abort(500, description="Error while updating DB with team")
    
    @route('/<int:team_id>', methods=['PUT'])
    def update_team_REST(self, team_id):
        """RESTful implementation of update team with PUT request
        """
        req = request.get_json()
        if not req or not all(item in req for item in ["name", "description", "admin"]):
            abort(400, description="Incorrect request body")
        return self._update_team_helper(team_id, req['name'], req['description'], req['admin'])
    
    @route('/update', methods=['POST'])
    def update_team(self) -> str:
        req = request.get_json()
        if not req or not all(item in req for item in ['id', 'team']) or not all(item in req['team'] for item in ['name', 'description', 'admin']):
            abort(400, description="Incorrect request body")
        return self._update_team_helper(req['id'], req['team']['name'], req['team']['description'], req['team']['admin'])
    
    #TODO: Add restful implementation
    @route('/add_users', methods=['POST'])
    def add_users_to_team(self):
        req = request.get_json()
        team = self._get_team_by_id(req['id'])
        for user_id in req['users']:
            user = self._get_user_by_id(user_id)
            if user not in team.users:
                if len(team.users) < 50:
                    team.users.append(user)
                    db.session.commit()
                else:
                    try:
                        db.session.commit()
                    except:
                        abort(500, description="Error while updating database")
                    return "Team can hold maximum 50 users!"
        try:
            db.session.commit()
        except:
            abort(500, description="Error while updating database")
        return "201"
    
    #TODO: Add restful implementation
    @route('/remove_users', methods=['POST'])
    def remove_users_from_team(self):
        req = request.get_json()
        team = self._get_team_by_id(req['id'])
        for user_id in req['users']:
            user = self._get_user_by_id(user_id)
            if len(team.users) > 1 and user in team.users:
                team.users.remove(user)
                #If admin user is removed, then assign a random user as new admin
                if team.admin == user:
                    team.admin = random.choice(team.users)
            elif len(team.users) == 1:
                try:
                    db.session.commit()
                except:
                    abort(500, description="Error while updating database")
                return "Team must have minimum 1 user"
        try:
            db.session.commit()
        except:
            abort(500, description="Error while updating database")
        return "201"
    
    @route('/<int:team_id>/users', methods=['GET'])
    def list_team_users_REST(self, team_id):
        """RESTful implementation of GET users in team"""
        team = self._get_team_by_id(team_id)
        return jsonify([user.list_users_for_team() for user in team.users])
    
    @route('/users', methods=['POST'])
    def list_team_users(self):
        try:
            req = request.get_json()
            return self.list_team_users_REST(req['id'])
        except:
            abort(400, description="Incorrect request body")
            
        