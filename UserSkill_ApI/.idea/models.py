"""
    models.py
    ---------
    Defining all required models here - tbl_lms_user, tbl_lms_skill_master, tbl_lms_userskill_map

"""

from database import db


class User(db.Model):
    __tablename__ = 'tbl_lms_user'
    user_id = db.Column(db.String(10), primary_key=True)
    user_first_name = db.Column(db.String(80), nullable=False)
    user_last_name = db.Column(db.String(80), nullable=False)
    user_phone_number = db.Column(db.Numeric, nullable=False)
    user_location = db.Column(db.String(80), nullable=False)
    user_time_zone = db.Column(db.String(20), nullable=False)
    user_linkedin_url = db.Column(db.String(80))
    user_edu_ug = db.Column(db.String(80))
    user_edu_pg = db.Column(db.String(80))
    user_comments = db.Column(db.String(3000))
    user_visa_status = db.Column(db.String(20), nullable=False)
    creation_time = db.Column(db.DateTime)
    last_mod_time = db.Column(db.DateTime)


class SkillMaster(db.Model):
    __tablename__ = 'tbl_lms_skill_master'
    skill_id = db.Column(db.BigInteger, primary_key=True)
    skill_name = db.Column(db.String(80), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    last_mod_time = db.Column(db.DateTime,nullable=False)


class SkillMap(db.Model):
    __tablename__ = 'tbl_lms_userskill_map'
    user_skill_id = db.Column(db.String(10), primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey(User.user_id), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey(SkillMaster.skill_id), nullable=False)
    months_of_exp = db.Column(db.Numeric, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)
    last_mod_time = db.Column(db.DateTime, nullable=False)