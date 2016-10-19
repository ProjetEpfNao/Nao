from commands import nao
import unittest

TEST_COMMAND = "test_command"
TEST_NOT_A_COMMAND = "not a command"


class TestNao(unittest.TestCase):

    def setUp(self):
        self.nao = nao.Nao()

    def tearDown(self):
        del self.nao

    def test_has_command(self):
        for c in self.nao.commands:
            assert self.nao.has_command(c)

    def test_execute_success(self):
        was_called = [False]
        def test_command():
            was_called[0] = True

        self.nao.commands[TEST_COMMAND] = test_command
        self.nao.execute(TEST_COMMAND)
        assert was_called[0]


    def test_execute_failure(self):
        self.assertRaises(KeyError, self.nao.execute, TEST_NOT_A_COMMAND)



if __name__ == "__main__":
    unittest.main()
