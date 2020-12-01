from PySense import SisenseRole
from PySense import PySenseAuthentication


def create_test_users(py_client, email, num, password):
    users = []
    for x in range(num):
        users.append(py_client.add_user(str(x) + '-' + email, SisenseRole.Role.VIEWER, password=password))
    return users


def generate_tokens(host, users, password):
    ret_array = []
    for user in users:
        ret_array.append(PySenseAuthentication.generate_token(host, user.get_user_name(), password))
    return ret_array



