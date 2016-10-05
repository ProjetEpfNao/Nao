from client.password_manager import PasswordManager
import unittest
import os


class TestPasswordManager(unittest.TestCase):
    TEST_PATH = os.path.join(
        "client", "tests", "test_resources", "test_credentials")
    TEMP_TEST_PATH = os.path.join(
        "client", "tests", "test_resources", "temp_test_credentials")

    def test_save(self):
        p_mgr = PasswordManager(self.TEMP_TEST_PATH)
        p_mgr.save("TEST_USERNAME", "TEST_PASSWORD")

        try:
            with open(self.TEMP_TEST_PATH, "r") as f:
                data = f.read()
        except IOError:
            assert False, "Failed to open saved test file."

        assert "TEST_USERNAME" in data
        assert "TEST_PASSWORD" in data

    def test_load_success(self):
        p_mgr = PasswordManager(self.TEST_PATH)
        try:
            p_mgr.load()
        except Exception as e:
            assert False, e.__doc__

        assert p_mgr.username == "username"
        assert p_mgr.password == "password"

    def test_load_no_file(self):
        p_mgr = PasswordManager(self.TEMP_TEST_PATH)
        self.assertRaises(IOError, p_mgr.load)

    def tearDown(self):
        try:
            with open(self.TEMP_TEST_PATH, "r") as f:
                pass
            os.remove(self.TEMP_TEST_PATH)
        except IOError:
            pass

if __name__ == "__main__":
    unittest.main()
