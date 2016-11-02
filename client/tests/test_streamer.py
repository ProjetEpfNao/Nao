from client import streamer
import unittest
import requests


TEST_URL = "test url"
TEST_DATA = b"this is my binary data"


class MockFrame(object):

    def get_data(self):
        return TEST_DATA


class MockFeed(object):

    def get_next_frame(self):
        return MockFrame()

class MockEmptyFeed(object):

    def get_next_frame(self):
        return None


class TestStreamer(unittest.TestCase):

    def setUp(self):
        Session = requests.Session
        mock_feed = MockFeed()
        self.streamer = streamer.Streamer(mock_feed, Session(), TEST_URL)

    def tearDown(self):
        del self.streamer

    def test_post_next_frame(self):
        def post(url, *args, **kwargs):
            assert kwargs["data"] == b"this is my binary data"
            assert url == TEST_URL
        self.streamer.session.post = post
        self.streamer.post_next_frame()


    def test_post_next_frame_no_frame(self):
        def post(url, *args, **kwargs):
            assert False
        self.streamer.session.post = post
        self.streamer.feed = MockEmptyFeed()
        self.streamer.post_next_frame()


if __name__ == "__main__":
    unittest.main()
