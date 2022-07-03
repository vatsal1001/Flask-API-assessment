from flask import request, jsonify, abort
from flask_classful import FlaskView, route

from datetime import datetime

from app.user_base import UserBase
from app.models.user_model import UserRecord
from app import db

class UserRoutes(FlaskView, UserBase):
    """
    Routes implementation for a user. Extends UserBase class.
    """
    def _get_user_by_id(self, id):
        return UserRecord.query.filter_by(id=id).first_or_404(description=f"There is no user with id={id}")
    
    @route('/', methods=["GET"])
    def list_users(self):
        try:
            users = UserRecord.query.all()
        except:
            abort(500, description="Error in obtaining records from user")
        return jsonify([user.list_user() for user in users])
    
    @route('/', methods=['POST'])
    def create_user(self):
        req = request.get_json()
        if not req or not all(item in req for item in ["name", "display_name"]):
            abort(400, description="Incorrect parameters in request body")
        creation_time = datetime.now()
        id = int(creation_time.timestamp())
        new_user = UserRecord(
            name=req['name'],
            display_name=req['display_name'],
            id=id,
            creation_time=creation_time
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            abort(500, description="Error while adding new user to DB")
        return jsonify({"id": id})
    
    @route('/<int:user_id>', methods=['GET'])
    def describe_user_REST(self, user_id):
        """RESTful method to GET each user. Absolute path is /user/<user_id>, which returns description of user
        """
        user = self._get_user_by_id(user_id)
        return jsonify(user.describe())

    @route('/describe', methods=['POST'])
    def describe_user(self) -> str:
        try:
            req = request.get_json()
            return self.describe_user_REST(req['id'])
        except:
            abort(400, description="Incorrect request body at /describe")

    def _update_user_helper(self, user_id, name, display_name):
        """Helper function which takes id, name and display_name and updates DB
        """
        user = self._get_user_by_id(user_id)
        user.name = name
        user.display_name = display_name
        try:
            db.session.commit()
            return '201'
        except:
            return abort(500, description="Error while updating user in DB")

    @route('/<int:user_id>', methods=['PUT'])
    def update_user_REST(self, user_id):
        """RESTful implementation of update user by using PUT request
        """
        try:
            req = request.get_json()
            return self._update_user_helper(user_id, req['name'], req['display_name'])
        except:
            abort(400, description="Incorrect request body")
    
    @route('/update', methods=['POST'])
    def update_user(self) -> str:
        try:
            req = request.get_json()
            return self._update_user_helper(req['id'], req['user']['name'], req['user']['display_name'])
        except:
            abort(400, description="Incorrect request body")
    
    @route('/<int:user_id>/teams', methods=['GET'])
    def get_user_teams_REST(self, user_id) -> str:
        """RESTful implementation of obtaining teams for a particular user with GET request
        """
        user = self._get_user_by_id(user_id)
        return jsonify([team.list_teams_for_user() for team in user.teams])
    
    @route('/teams', methods=['POST'])
    def get_user_teams(self) -> str:
        try:
            req = request.get_json()
            return self.get_user_teams_REST(req['id'])
        except:
            abort(400, description="Incorrect request body")