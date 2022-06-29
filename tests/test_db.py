# tests.py

import unittest
from peewee import *

from app import TimelinePost, get_time_line_post

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

    def test_timeline_post(self):
        # Create 2 timeline posts.
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello world, I\'m John!')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello world, I\'m Jane!')
        assert second_post.id == 2
        # TODO: Get timeline posts and assert that they are correct
        created_posts = [first_post, second_post]
        response = get_time_line_post()['timeline_posts']
        timeline_posts = [response[1], response[0]]

        for i in range(2):
            assert created_posts[i].name == timeline_posts[i]['name']
            assert created_posts[i].email == timeline_posts[i]['email']
            assert created_posts[i].content == timeline_posts[i]['content']
