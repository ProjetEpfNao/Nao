from client import client, rest_api, client_exception
import unittest
import os
import requests

TEST_MODE_SUCCESS = "success"
TEST_MODE_SUCCESS_NO_COMMAND = "success_no_command"
TEST_MODE_FAILURE_CONNECTION = "failure_1"
TEST_MODE_FAILURE_SERVER = "failure_2"
TEST_USER = "test_user"
TEST_PASS = "test_pass"
TEST_KEY = "data_key"
TEST_DATA = "data_content"
TEST_URL_SUCCESS = "test_url_success"
TEST_URL_FAILURE = "test_url_failure"
TEST_COMMAND = "test_command_type"
TEST_NOT_A_COMMAND = "test_not_a_command"


class MockResponse(object):

    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


class MockRobot(object):

    def __init__(self):
        self.execute_called = False
        self.execute_c = None
        self.execute_a = None

    def execute(self, c, *a):
        self.execute_called = True
        self.execute_c = c
        self.execute_a = a

    def has_command(self, c):
        if c == TEST_COMMAND:
            return True
        return False

    def set_command_callback(self, c):
        pass


def mock_get(session, url, *args):
    if session.test_mode == TEST_MODE_FAILURE_CONNECTION:
        return MockResponse(404, {})

    # if url == rest_api.CREDENTIALS_URL:
    #     return MockResponse(200,
    #                         {rest_api.STATUS_KEY: rest_api.SUCCESS,
    #                          rest_api.CRED_USER_KEY: TEST_USER,
    #                          rest_api.CRED_PASS_KEY: TEST_PASS})

    if url == TEST_URL_SUCCESS:
        return MockResponse(200,
                            {rest_api.STATUS_KEY: rest_api.SUCCESS,
                             TEST_KEY: TEST_DATA})

    if url == TEST_URL_FAILURE:
        return MockResponse(200,
                            {rest_api.STATUS_KEY: rest_api.FAILURE,
                             rest_api.ERROR_KEY: TEST_DATA})

    if url == rest_api.COMMAND_URL:
        if session.test_mode == TEST_MODE_SUCCESS_NO_COMMAND:
            return MockResponse(200,
                                {rest_api.STATUS_KEY: rest_api.SUCCESS,
                                 rest_api.COMMAND_TYPE_KEY: ""})
        return MockResponse(200,
                            {rest_api.STATUS_KEY: rest_api.SUCCESS,
                             rest_api.COMMAND_TYPE_KEY: TEST_COMMAND})

    return MockResponse(404, {})


def mock_post(session, url, **kwargs):
    if url == rest_api.LOGIN_URL:
        if session.test_mode == TEST_MODE_SUCCESS:
            return MockResponse(200,
                                {rest_api.STATUS_KEY: rest_api.SUCCESS})
        else:
            return MockResponse(200,
                                {rest_api.STATUS_KEY: rest_api.FAILURE,
                                 rest_api.ERROR_KEY: TEST_DATA})

    if url == rest_api.REGISTER_URL:
        return MockResponse(200,
                            {rest_api.STATUS_KEY: rest_api.SUCCESS})

    return MockResponse(404, {})


class TestClient(unittest.TestCase):

    def setUp(self):
        Session=requests.Session
        Session.get=mock_get
        Session.post=mock_post
        robot=MockRobot()
        self.c=client.Client(robot, Session)
        self.c.session.test_mode=TEST_MODE_SUCCESS

    def tearDown(self):
        del self.c

    def test_init_password_manager(self):
        self.c.init_password_manager()

        assert self.c.password_manager != None
        assert self.c.password_manager.username != None
        assert self.c.password_manager.password != None

    # def test_fetch_new_credentials_success(self):
    #     user, passwd = self.c.fetch_new_credentials()

    #     assert user == TEST_USER
    #     assert passwd == TEST_PASS

    # def test_fetch_new_credentials_bad_status_code(self):
    #     self.c.session.test_mode = TEST_MODE_FAILURE_CONNECTION
    #     self.assertRaises(client_exception.ConnectionError,
    #                       self.c.fetch_new_credentials)

    def test_fetch_data_success(self): #TODO: Rework to go test parse_resp instead and light fetch_data, post_data tests
        self.c.session.test_mode=TEST_MODE_SUCCESS
        body=self.c.fetch_data(TEST_URL_SUCCESS)
        assert TEST_KEY in body
        assert body[TEST_KEY] == TEST_DATA

    def test_fetch_data_http_error(self):
        self.c.session.test_mode=TEST_MODE_FAILURE_CONNECTION
        self.assertRaises(client_exception.ConnectionError,
                          self.c.fetch_data, TEST_URL_SUCCESS)

    def test_fetch_data_server_error(self):
        self.c.session.test_mode=TEST_MODE_SUCCESS
        self.assertRaises(client_exception.ServerError,
                          self.c.fetch_data, TEST_URL_FAILURE)

    def test_fetch_command_success_command(self):
        self.c.session.test_mode=TEST_MODE_SUCCESS
        command=self.c.fetch_command()
        assert command.type == TEST_COMMAND

    def test_fetch_command_success_no_command(self):
        self.c.session.test_mode=TEST_MODE_SUCCESS_NO_COMMAND
        command=self.c.fetch_command()
        assert command == None

    def test_execute_on_robot_success(self):
        self.c.execute_on_robot(TEST_COMMAND)
        assert self.c.robot.execute_called
        assert self.c.robot.execute_c == TEST_COMMAND
        assert self.c.robot.execute_a == ()

    def test_execute_on_robot_no_such_command(self):
        self.assertRaises(client_exception.NoSuchCommandError,
                          self.c.execute_on_robot, TEST_NOT_A_COMMAND)


if __name__ == "__main__":
    unittest.main()
