import os
from telnetlib import STATUS
from flask import Flask, render_template, request, redirect, Response
from dotenv import load_dotenv
from peewee import*
import datetime
from playhouse.shortcuts import model_to_dict
import re

load_dotenv()

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), 
        user=os.getenv("MYSQL_USER"), 
        password=os.getenv("MYSQL_PASSWORD"), 
        host=os.getenv("MYSQL_HOST"), 
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

print(mydb)

def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)

class Person:
    def __init__(self, _name, _hobbies, _workExperience, _education, _aboutMe, _travelMapURL, _profileImageURL="./static/img/logo.jpg"):
        self.name = _name
        self.hobbies = _hobbies
        self.workExperience = _workExperience
        self.education = _education
        self.aboutMe = _aboutMe
        self.travelMapURL = _travelMapURL
        self.profileImageURL = _profileImageURL

class WorkExperience:
    def __init__(self, _startDate, _endDate, _organization, _role, _roleDescriptions = ""):
        self.startDate = _startDate
        self.endDate = _endDate
        self.organization = _organization
        self.role = _role
        self.roleDescription = _roleDescriptions

class Education:
    def __init__(self, _institution, _completionDate, _degree):
        self.institution = _institution
        self.completionDate = _completionDate
        self.degree = _degree

class Hobby:
    def __init__(self, _name, _pictureURLs = "", _description = ""):
        self.name = _name
        self.pictureURLs = _pictureURLs
        self.description = _description

def GetPeople():
                
    Maurice = Person("Maurice Korish"
                , [Hobby("Model United Nations", ["./static/img/Maurice/modelun.jpg"])
                    , Hobby("Track/Cross Country", ["./static/img/Maurice/track.jpg"])
                    , Hobby("Soccer", [])]
                , [WorkExperience("January 2019", "May 2021", "FeedBot Project", "Lead Developer", "With a partner, I created a device that uses facial recognition technology to guide a robotic-feeding arm to an individual's mouth.")]
                , [Education("Stanford University", "May 2026", "Bachelor's of Science in Computer Science")]
                , "Hi! My name is Maurice Korish, and I am from New Jersey. I'm very interested in math, physics, and computer science, and I would love to work on developing technologies that can enhance our understanding of the world we live in."
                ,"", "./static/img/Maurice/maurice.jpg")

    people = [Maurice]
    return people

@app.route('/')
def index():
    return render_template('index.html', title="The Home Page", url=os.getenv("URL"))


@app.route('/about')
def aboutme():
    return render_template('about.html', title="About Me", type="About Me", people=GetPeople(),  url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", type="Our Hobbies", people=GetPeople(),  url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map of the Places We Have Visited",  url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline Post")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        invalidName = Response("Invalid name")
        invalidName.status_code = 400
        name = request.form['name']
        if name == "":
            return invalidName
    except KeyError:
        return invalidName

    try:
        invalidContent = Response("Invalid content")
        invalidContent.status_code = 400
        content = request.form['content']
        if content == "":
            return invalidContent
    except KeyError:
        return invalidContent

    try:
        invalidEmail = Response("Invalid email")
        invalidEmail.status_code = 400
        email = request.form['email']
        if email == "" or (not checkEmail(email)):
            return invalidEmail
    except KeyError:
        return invalidEmail

    #redirect('/timeline')
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post) 




@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }