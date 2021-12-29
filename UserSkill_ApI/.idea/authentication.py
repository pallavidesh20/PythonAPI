# from flask_httpauth import HTTPBasicAuth
#
# auth = HTTPBasicAuth()
# USER_CREDENTIALS ={"admin":"password"}
#
#
# @auth.verify_password
# def verify(username, password):
#     if not (username and password):
#         return False
#     return username in USER_CREDENTIALS.keys() and USER_CREDENTIALS.get(username) == password


from flask_httpauth import HTTPBasicAuth
from settings import USER_NAME, PASSWORD

auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return username == USER_NAME and password == PASSWORD

