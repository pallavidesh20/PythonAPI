
"""
    user_skills_resource.py
    -----------------
    Contains the main business logic for the endpoints /User_skills and /User_skills/<id>
    The main implementation lies within class UsersResource for the CRUD functionalities
"""

import datetime
from flask_restful import Resource
from flask import request
from sqlalchemy import func
from database import db
from models import User
from models import SkillMaster
from models import SkillMap
from authentication import auth
from sqlalchemy import and_
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
"""
--------------------------------------------------------------------------------------------------------
 ***********Function to search user_id from the users table**************************
--------------------------------------------------------------------------------------------------------
"""
def user_search_only(id):
    user = User.query.get(id)
    if user is None:
        return {'message': 'User Not Found'}
    else:
        return {'message': 'User Found'}
"""
-----------------------------------------------------------------------------------------------------
*************function to search skill_id from the skill master table******************
-----------------------------------------------------------------------------------------------------
"""
def skill_search_only(id):
    skill = SkillMaster.query.get(id)
    if skill is None:
        return {'message': 'Skill Not Found'}
    else:
        return {'message': 'Skill Found'}
"""
---------------------------------------------------------------------------------------------------------
*************function to search skill_id and user_id from the skill master and users table******************
----------------------------------------------------------------------------------------------------------
"""

def userskill_search_only(*args):
    usk = SkillMap.query.filter(and_(SkillMap.user_id == args[0], SkillMap.skill_id == args[1]))
    usk_list = []
    for skillmap in usk:
        usk_data = {'userskillid' :skillmap.user_skill_id}
        usk_list.append(usk_data)
        print(usk_list)
    if len(usk_list) == 0:
        return {'message' : 'UserSkills Not Found'}
    else:
        return {'message' : 'UserSkillmap found'}

def user_skill_id_search_only(id):
    uskid = SkillMap.query.get(id)
    if uskid is None:
        return {'message': 'UserSkillID Not Found'}
    else:
        return {'message': 'UserSkillID Found'}


class UserSkillsResource(Resource):

    @auth.login_required
    def get(self, id=None):
        if not id:
            userskills = SkillMap.query.all()
            userskill_list = []
            for userskill in userskills:
                userskill_data = {'user_skill_id': str(userskill.user_skill_id), 'user_id': str(userskill.user_id), 'Skill_id' : str(userskill.skill_id), 'months_of_exp': str(userskill.months_of_exp)}
                userskill_list.append(userskill_data)
            return {'UserSkillMapping' : userskill_list}, 200

        userskills = SkillMap.query.get(id)
        if userskills is None:
            return {'message': 'User Skill Mapping Not Found'}, 404

        return {'user_skill_id': str(userskills.user_skill_id), 'user_id': str(userskills.user_id), 'Skill_id' : int(userskills.skill_id), 'months_of_exp': int(userskills.months_of_exp)}, 200

    @auth.login_required
    def post(self):
        blank_field_check = '' in (str(request.json['user_id']),request.json['Skill_id'], request.json['months_of_exp'])
        if blank_field_check:
            return {'message' : 'Failed to create due to invalid data'},400
        if request.is_json:
            user_id= (str(request.json['user_id']))
            if type(user_id)is None:
               return {'message':'Failed to create due to invalid user Id'}, 400
            skill_id = (request.json['Skill_id'])
            if type(skill_id) in (str, bool, None):
                return {'message':'Failed to create due to invalid skill Id'}, 400
            months_of_exp = (request.json['months_of_exp'])
            if type(months_of_exp) in (str,None):
                return {'message':'Failed to create due to invalid months of experience'}, 400
            max_id = str(db.session.query(func.max(SkillMap.user_skill_id)).scalar())
            new_user_skill_id = self._generate_user_skill_id(max_id)
            usersearch = user_search_only(user_id)
            skillsearch = skill_search_only(skill_id)
            userskillsearch = userskill_search_only(user_id, skill_id)
            #return  userskillsearch
            if (usersearch['message'] == 'User Not Found'):
                return {'message' : 'Failed to create due to invalid user Id'},400
            elif (skillsearch['message'] == 'Skill Not Found'):
                return {'message' : 'Failed to create due to invalid skill Id'},400
            elif (userskillsearch['message'] == 'UserSkillmap found'):
                return {'message' : 'Failed to create as UserSkillMap already exists'},400
            elif (usersearch['message'] == 'User Found') and skillsearch['message'] == 'Skill Found':
                userskill = SkillMap(user_skill_id = new_user_skill_id, user_id= user_id, skill_id= skill_id, months_of_exp = months_of_exp, creation_time= datetime.datetime.now(), last_mod_time= datetime.datetime.now())
                db.session.add(userskill)
                db.session.commit()
                return {'user_skill_id': str(userskill.user_skill_id), 'user_id': str(userskill.user_id), 'Skill_id' : int(userskill.skill_id), 'months_of_exp': int(userskill.months_of_exp), 'message':'Successfully Created'}, 201

    @auth.login_required
    def put(self,id):
        blank_field_check = request.json['months_of_exp']
        if type(blank_field_check) in (str, bool):
            return {'message' : 'Failed to update due to invalid months of experience'},400
        if request.is_json:
            months_of_exp = (request.json['months_of_exp'])
            uskidsearch = user_skill_id_search_only(id)
            if (uskidsearch['message'] == 'UserSkillID Not Found'):
                return {'message' : 'User Skill Mapping Not Found'},404
            elif (uskidsearch['message'] == 'UserSkillID Found'):
                usk = SkillMap.query.filter(SkillMap.user_skill_id == id).first()
                usk.months_of_exp=months_of_exp
                usk.creation_time= datetime.datetime.now()
                usk.last_mod_time= datetime.datetime.now()
                db.session.commit()
                return {'user_skill_id': str(usk.user_skill_id), 'user_id': str(usk.user_id), 'Skill_id' : int(usk.skill_id), 'months_of_exp': int(usk.months_of_exp),'message':'Successfully Updated'}, 201


    @auth.login_required
    def delete(self, id):
        userskill = SkillMap.query.get(id)
        if not userskill:
            return  {'message': 'User skill Map Not Found'}, 404
        db.session.delete(userskill)
        db.session.commit()
        return {'message' : 'Successfully deleted'}, 200


    def _generate_user_skill_id(self,max_id):
        auto_id_num = int(max_id.split('US')[1]) + 1
        new_user_skill_id = 'US' + str(auto_id_num)
        return new_user_skill_id