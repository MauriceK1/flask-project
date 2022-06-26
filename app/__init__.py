import os
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from peewee import*
import datetime
from playhouse.shortcuts import model_to_dict


load_dotenv()

app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"), user=os.getenv("MYSQL_USER"), password=os.getenv("MYSQL_PASSWORD"), host=os.getenv("MYSQL_HOST"), port=3306)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    create_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

print(mydb)

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
    Lucas = Person("Lucas Cancio"
                , [Hobby("game development", ["./static/img/lucas/gameDev02.PNG", "./static/img/lucas/gameDev03.PNG"], "I enjoy making games, mainly the programming aspect since I am not the best artist. You can check out some of the things I have made on my Itch.io page.")
                    , Hobby("martial arts", ["./static/img/lucas/tkd.PNG"], "I like doing different forms of martial arts, including Taekwondo, Brazilian Jiu Jitsu, and kick boxing.")
                    , Hobby("outdoors stuff", ["./static/img/lucas/outdoors01.jpg", "./static/img/lucas/outdoors02.jpg", "./static/img/lucas/outdoors03.jpg"], "I enjoy biking and hiking in a nature park near my home.")]
                , [WorkExperience("May 2020", "August 2020", "TheCoderSchool", "Programming Tutor", "I tutored kids on how to program using C++, Python, and Scratch.")
                    , WorkExperience("June 2021", "September 2021", "Machine Intelligence Lab @ UF", "Undergraduate Researcher", "I mainly focused on documenting an autonomous submarine's simulation software.")]
                , [Education("University of Florida", "May 2023", "Bachelor's of Science in Computer Science")]
                , "Hello everyone! I am a 4th year CS major at University of Florida in the USA. I am pursuing becoming a professional software developer with a focus on web development. From what I have learned so far from this program, I am now also considering being a production engineer. I love programming and the power it gives me to create things like games and what ever cool app ideas I can imagine."
                , ""
                , "./static/img/lucas/lucas.jpg")

    Luis = Person("Luis Moraguez"
                , [Hobby("kayaking", ["./static/img/luis/kayak.jpg"], "I love to kayak challenging paddling trails around Florida.")
                    , Hobby("running", ["./static/img/luis/running.jpg"], "I love running long distance.")
                    , Hobby("camping", ["./static/img/luis/camping.jpg"], "I love connecting with nature and camping and beautiful areas around the US.")]
                , [WorkExperience("March 2017", "April 2021", "City of Kissimmee Information Technology", "Enterprise Applications Administrator", "Responsible for implementing, maintaining, and upgrading all of the city's Enterprise Public Safety applications. Projects: Custom developed interface to send live accident data to Waze, implemented Workforce Telestaff, implemented export from OneSolutionCAD to ESO, custom developed forms and reports for various needs of Police and Fire Departments, implemented body camera system for Police, implemented SSO for body camera system, custom developed integration between OneSolutionCAD and body camera system, custom developed self-service web app for Police. Also responsible for mapping departmental workflow processes, testing the applications, working with vendors to resolve software bugs or issues, creating documentation, training staff, and evaluating new features or products.")
                    ,WorkExperience("April 2015", "March 2017", "City of Kissimmee Information Technology", "Computer Specialist", "Handled all the trouble calls from every department in the city, including public safety departments by providing onsite and remote support for users. Responsible for the configuration of new equipment purchased for each department. Responsible for handling on-call and after-hours issues from public safety departments on a rotation. Effectively communicated with 3 rd party support from hardware/software vendors, partners, and technical support. Maintained accurate documentation of hardware to be deployed or disposed of, and documentation of all interactions with users and the steps taken to resolve their issues. Maintained positive working relationships with users throughout the city departments.")]
                , [Education("Florida Polytechnic University", "May 2023", "Bachelor's of Science in Computer Science")
                    ,Education("Valencia College", "May 2017", "Associate of Science in Network Engineering")
                    ,Education("Valencia College", "May 2017", "Associate of Science in Cyber Security")]
                , "Hi everyone, my name is Luis Moraguez. I was born in raised in Kissimmee, FL. I've always had a passion for technology. I've spent the last 10+ years working professionally in the IT field, and I've recently decided to switch to Computer Science because I want to build technology to help people. When I'm not in front of the computer, I love to be outdoors!"
                , ""
                , "./static/img/luis/profile.jpg")
                
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
    return render_template('index.html', title="Home Page", url=os.getenv("URL"))


@app.route('/about')
def aboutme():
    return render_template('about.html', title="About Me", type="About Me", people=GetPeople(),  url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", type="Our Hobbies", people=GetPeople(),  url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.html', title="Map of Places We Have Visited",  url=os.getenv("URL"))

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline Post")

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    
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
TimelinePost.select().order_by(TimelinePost.create_at.desc())
        ]
    }