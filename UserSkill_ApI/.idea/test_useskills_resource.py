"""
    TDD test cases built from gherkins for the User Skills API.
    These functions test the get, post, put and delete methods
    of UseSkillsResource Class which are the units to be built to support url/UserSkills and ur/UserSkills/<id> endpoints
"""
from userskills_resource import UserSkillsResource
from constants import USERSKILLS_ENDPOINT
from contantsTDD import USER_ID, SKILL_ID, MONTHS_OF_EXP, INVALID_USERSKILLID, VALID_USERSKILLID, \
    MAX_USER_SKILL_ID, AUTO_GEN_USER_SKILL_ID, VALID_USERSKILLID_2, USER_ID_2, SKILL_ID_2, MONTHS_OF_EXP_2, USER_ID_3, \
    VALID_USERSKILLID_3, SKILL_ID_3, MONTHS_OF_EXP_3, INVAD_MONTHS_OF_EXP_4, VALID_USERSKILLID_5


""" ------------------Test cases for Get method ()---------------------------"""

def test_get_all_userskills_unauth_pwd(client, invalid_password):
    response = client.get(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + invalid_password})
    assert response.status_code == 401

def test_get_all_userskills_unauth_user(client, invalid_user):
    response = client.get(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + invalid_user})
    assert response.status_code == 401

def test_get_all_userskills_noauth(client):
    response = client.get(f"{USERSKILLS_ENDPOINT}")
    assert response.status_code == 401

def test_get_all_userskills(client, valid_auth):
    response = client.get(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 200

def test_get_one_userskills(client, valid_auth):
    response = client.get(f"{USERSKILLS_ENDPOINT}/{VALID_USERSKILLID_2}", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 200
    print(response.json)
    assert response.json['user_skill_id'] == VALID_USERSKILLID_2
    assert response.json['user_id'] == USER_ID_2
    assert response.json['Skill_id'] == SKILL_ID_2
    assert response.json['months_of_exp'] == MONTHS_OF_EXP_2

def test_get_invalid_userskillid(client, valid_auth):
    response = client.get(f"{USERSKILLS_ENDPOINT}/{INVALID_USERSKILLID}", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 404
    assert response.json['message'] == 'User Skill Mapping Not Found'

def test_get_decimal_userskillid(client, valid_auth):
    response = client.get(f"{USERSKILLS_ENDPOINT}/9.9", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 404
    assert response.json['message'] == 'User Skill Mapping Not Found'

def test_get_alphanumeric_userskillid(client, valid_auth):
    response = client.get(f"{USERSKILLS_ENDPOINT}/abc123", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 404
    assert response.json['message'] == 'User Skill Mapping Not Found'

""" ------------------Test cases for Post method ()---------------------------"""

def test_post_userskills(client, valid_auth):
    create_userskill_json = {"user_id": "U03", "Skill_id": 5, "months_of_exp": 20}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 201
    assert response.json['user_skill_id'] == "US136"
    assert response.json['user_id'] == "U03"
    assert response.json['Skill_id']  == 5
    assert response.json['months_of_exp']  == 20
    assert response.json['message'] == 'Successfully Created'

def test_post_alphnumkillid(client, valid_auth):
    create_userskill_json = {"user_id": "U09", "Skill_id": "abc123", "months_of_exp": 17}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create due to invalid skill Id'

def test_post_nullskillid(client, valid_auth):
    create_userskill_json = {"user_id": "U09", "Skill_id": "", "months_of_exp": 17}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create due to invalid data'

def test_post_nulluserid(client, valid_auth):
    create_userskill_json = {"user_id": "", "Skill_id": 2, "months_of_exp": 17}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create due to invalid data'

def test_post_alphnumexperience(client, valid_auth):
    create_userskill_json = {"user_id": "U09", "Skill_id": 6, "months_of_exp": "abc123"}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create due to invalid months of experience'

def test_post_nullexperience(client, valid_auth):
    create_userskill_json = {"user_id": "U09", "Skill_id": 6, "months_of_exp": ""}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create due to invalid data'

def test_post_existingid(client, valid_auth):
    create_userskill_json = {"user_id": "U09", "Skill_id": 2, "months_of_exp": 18}
    response = client.post(f"{USERSKILLS_ENDPOINT}", headers={"Authorization": "Basic " + valid_auth},
                           json=create_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to create as UserSkillMap already exists'

""" ------------------Test cases for Put method ()---------------------------"""

def test_put_userskills(client, valid_auth):
    update_userskill_json = { "months_of_exp": MONTHS_OF_EXP_3 }

    response = client.put(f"{USERSKILLS_ENDPOINT}/{VALID_USERSKILLID_3}", headers={"Authorization": "Basic " + valid_auth},
                           json=update_userskill_json)
    assert response.status_code == 201
    assert response.json['user_skill_id'] == VALID_USERSKILLID_3
    assert response.json['user_id'] ==  USER_ID_3
    assert response.json['Skill_id']  ==  SKILL_ID_3
    assert response.json['months_of_exp']  == MONTHS_OF_EXP_3
    assert response.json['message'] == 'Successfully Updated'

def test_put_invaliduserskills(client, valid_auth):
    update_userskill_json = {"months_of_exp": MONTHS_OF_EXP_3}

    response = client.put(f"{USERSKILLS_ENDPOINT}/{INVALID_USERSKILLID}", headers={"Authorization": "Basic " + valid_auth},
                          json=update_userskill_json)
    assert response.status_code == 404
    assert response.json['message'] == 'User Skill Mapping Not Found'

def test_put_userskills_invalidexp(client, valid_auth):
    update_userskill_json = {"months_of_exp": INVAD_MONTHS_OF_EXP_4}

    response = client.put(f"{USERSKILLS_ENDPOINT}/{VALID_USERSKILLID_3}", headers={"Authorization": "Basic " + valid_auth},
                          json=update_userskill_json)
    assert response.status_code == 400
    assert response.json['message'] == 'Failed to update due to invalid months of experience'

""" ------------------Test cases for Delete method ()--------------------------------------"""

def test_delete_one_userskills(client, valid_auth):
    response = client.delete(f"{USERSKILLS_ENDPOINT}/{VALID_USERSKILLID_5}", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 200
    assert response.json['message'] == 'Successfully deleted'

def test_delete_invalid_userskillid(client, valid_auth):
    response = client.delete(f"{USERSKILLS_ENDPOINT}/{INVALID_USERSKILLID}", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 404
    assert response.json['message'] == 'User skill Map Not Found'

def test_delete_decimal_userskillid(client, valid_auth):
    response = client.delete(f"{USERSKILLS_ENDPOINT}/9.9", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 404
    assert response.json['message'] == 'User skill Map Not Found'

def test_delete_alphanumeric_userskillid(client, valid_auth):
    response = client.delete(f"{USERSKILLS_ENDPOINT}/abc12", headers={"Authorization": "Basic " + valid_auth})
    assert response.status_code == 404
    assert response.json['message'] == 'User skill Map Not Found'

""" ------------------Test cases for autogen user skill id method ()---------------------------"""

def test_autogenerate_userskillid():
    userskills_resource = UserSkillsResource()
    auto_user_skill_id = userskills_resource._generate_user_skill_id(MAX_USER_SKILL_ID)
    assert auto_user_skill_id == AUTO_GEN_USER_SKILL_ID







