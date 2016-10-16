from client import client, rest_api, client_exception
import unittest
import os
import requests

TEST_MODE_SUCCESS = "success"
TEST_MODE_FAILURE = "failure"
TEST_USER = "test_user"
TEST_PASS = "test_pass"


class MockResponse(object):

    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data


class MockRobot(object):

    def set_command_callback(self, c):
        pass


def mock_get(session, url, *args):
    if session.test_mode == TEST_MODE_FAILURE:
        return MockResponse(404, {})
    if url == rest_api.CREDENTIALS_URL:
        return MockResponse(200, {rest_api.CRED_USER_KEY: TEST_USER, rest_api.CRED_PASS_KEY: TEST_PASS})
    return MockResponse(404, {})


class TestClient(unittest.TestCase):

    def setUp(self):
        Session = requests.Session
        Session.get = mock_get
        robot = MockRobot()
        self.c = client.Client(robot, Session)
        self.c.session.test_mode = TEST_MODE_SUCCESS

    def tearDown(self):
        del self.c

    def test_init_password_manager(self):
        self.c.init_password_manager()

        assert self.c.password_manager != None
        assert self.c.password_manager.username != None
        assert self.c.password_manager.password != None

    def test_fetch_new_credentials_success(self):
        user, passwd = self.c.fetch_new_credentials()

        assert user == TEST_USER
        assert passwd == TEST_PASS

    def test_fetch_new_credentials_bad_status_code(self):
        self.c.session.test_mode = TEST_MODE_FAILURE
        self.assertRaises(client_exception.ConnectionError,
                          self.c.fetch_new_credentials)


if __name__ == "__main__":
    unittest.main()
