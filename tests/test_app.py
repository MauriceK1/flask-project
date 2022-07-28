# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, post_time_line_post, timeline

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Home Page</title>" in html
        # TODO Add more tests relating to the home page
        assert "<img src=\"./static/img/logo.jpg\">" in html
        assert "<a class=\"nav-item nav-link\" href=\"/\">Hom</a>" in html
        assert "<a class=\"nav-item nav-link\" href=\"/about\">About Me</a>" in html
        assert "<a class=\"nav-item nav-link\" href=\"/hobbies\">Hobbies</a>" in html
        assert "<a class=\"nav-item nav-link\" href=\"/map\">Map</a>" in html
        assert "<a class=\"nav-item nav-link\" href=\"/timeline\">Timeline Post</a>" in html
        assert "<img src=\"./static/img/logo.svg\" />" in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0
        # TODO Add more tests relating to the /api/timeline_post GET and POST apis
        created_posts = [
            {
                'name': 'John Doe',
                'email': 'johndoe@gmail.com',
                'content': 'This is a sample post from John Doe!'
            },
            {
                'name': 'Jane Doe',
                'email': 'janedoe@gmail.com',
                'content': 'This is a sample post from Jane Doe!'
            }
        ]
        responses = []
        for i in range(2):
            responses.append(self.client.post("/api/timeline_post", data=created_posts[i]))
            assert responses[i].status_code == 200
            assert responses[i].is_json
            responses[i] = responses[i].get_json()
            assert created_posts[i]['name'] == responses[i]['name']
            assert created_posts[i]['email'] == responses[i]['email']
            assert created_posts[i]['content'] == responses[i]['content']

        get_response = self.client.get("/api/timeline_post")
        assert get_response.status_code == 200
        assert get_response.is_json
        get_response = get_response.get_json()
        assert "timeline_posts" in get_response
        response_list = get_response["timeline_posts"]
        assert len(created_posts) == len(response_list)

        for i in range(2):
            assert created_posts[i]['name'] == response_list[i * -1 + 1]['name']
            assert created_posts[i]['email'] == response_list[i * -1 + 1]['email']
            assert created_posts[i]['content'] == response_list[i * -1 + 1]['content']
        
        # TODO Add more tests relating to the timeline page
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Timeline Post</title>" in html
        assert "Enter Information:" in html
        assert "<button type=\"submit\" class=\"btn btn-primary\" style=\"margin-top: 10px\">Submit</button>" in html
        assert "<label for=\"name\">Name</label>" in html
        assert "<label for=\"email\">Email</label>" in html
        assert "<label for=\"\">Content</label>"  in html
        assert "Display Information:" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})  
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html