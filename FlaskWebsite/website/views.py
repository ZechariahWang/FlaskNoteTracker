from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
import json
import os
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup

views = Blueprint('views', __name__)

def api_get(url, params={}):
    headers = CaseInsensitiveDict()
    headers["accept-language"] = "en"
    headers["Authorization"] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiZjc5MzgwNmVlOTU3ZmEyYzkyODk3YTdjMTcxOGE1Zjc2ZDZhNTcxODJlM2U5NmI4Mjc5OWIwNjllMjE3ZDQ4ZjJmY2FlOTdjYmJmM2QzMDIiLCJpYXQiOjE2NzQ3OTg5OTAuMDk1NDkxOSwibmJmIjoxNjc0Nzk4OTkwLjA5NTQ5NTksImV4cCI6MjYyMTU3MDE5MC4wOTIwNDM5LCJzdWIiOiI4NDUxOSIsInNjb3BlcyI6W119.KglMyufEjUZ8WceNQJ2GMWj5e2qQsya1QPm7jHBhYg0cqOgCmWi2UqnaMqLsmJubv-Y5Mv-IWjkQ5E6bD8l57qGsvtGllvms_jW4KmdD8w9iDMo8YFNmuMN4OTt00gmOgOoBPZcSeYVwXJnQoX_WWOlxIyeGPKI11bxUNfJXr9xD4NhTG0wSQyS6yS53hh1XEJtDRzUw7Eeoq_PVWIzipmzOqeFnx2NxHOeRpNQj9dGKNBPiTy1M42wiNi8bErONBfwikddQsk_xN2ePfqC1zsM9qL34pWm3enNPqVn92zTzp1fUiwQcBdPttWt-Y52Gy-VUYVnm5ZMq8s5Xk8pB2op5k9EOTl1-8r1BnSYJepwsJSaDRr_JsuhwAvVTisemSKN7bM5dGjLcb8dr6peQLSXUMnedjmf2Kq3AjEOy-CeazL9tAOQ4kqHU75eNnWJek1J9ulSbuZiv3q3xNlKz_TWzLVItyKPB7JMZPqEmpoqnnUev1ZLNAYyZZDdG0sbRlnjP-Ad8paeoYSASpahoKMchc2FMVM3KaWa69XbKEQJ8sDsP3b0gLcXB_a_uq4NWMHm-0P9yqCGPOuz0NYzLGBfN-Kvq2GUzWxSbixxVp952ESdsiGIARq0yFn0c3Lvfp35UhjuggWHuFnGmVnqYCNjSMqBmWaP6K_BrxP39NMc"

    r = requests.get("https://www.robotevents.com/api/v2/" + url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(f"API Error: {r.status_code} {r.text}")
    return r.json()


def get_robot_name(team):
    r = requests.get(f"https://www.robotevents.com/teams/VRC/{team}")
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select('tr:-soup-contains("Robot Name:")')[0].select("td")[0].text

def get_skills_score(team):
    r = requests.get(f"https://www.robotevents.com/teams/VRC/{team}")
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select('tr:-soup-contains("World Skills Rank:")')[0].select("td")[0].text

def get_grade_level(team):
    r = requests.get(f"https://www.robotevents.com/teams/VRC/{team}")
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select('tr:-soup-contains("Grade Level:")')[0].select("td")[0].text

def get_location(team):
    r = requests.get(f"https://www.robotevents.com/teams/VRC/{team}")
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select('tr:-soup-contains("Location:")')[0].select("td")[0].text

def get_program(team):
    r = requests.get(f"https://www.robotevents.com/teams/VRC/{team}")
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select('tr:-soup-contains("Program:")')[0].select("td")[0].text

def get_awards(team):
    awardData = {}
    data = api_get(
        f"teams/{team.id}/awards",
        params={
            "season": "173",
        }
    )['data']
    for award in data:
        eventName = award['event']['name']
        eventCode = award['event']['code']
        eventName = eventName + "|" + eventCode
        if awardData.get(eventName, None) is None:
            awardData[eventName] = []
        awardData[eventName].append(award['title'])
    awards = []
    for event, awardList in awardData.items():
        eventData = event.split("|")
        awards.append(
            {"event": {"name": eventData[0], "code": eventData[1]}, "awards": awardList})
    print(awards)
    return awards

def get_awards(team):
    awardData = {}
    data = api_get(
        f"teams/{team}/awards",
        params={
            "season": "173",
        }
    )['data']
    for award in data:
        eventName = award['event']['name']
        eventCode = award['event']['code']
        eventName = eventName + "|" + eventCode
        if awardData.get(eventName, None) is None:
            awardData[eventName] = []
        awardData[eventName].append(award['title'])
    awards = []
    for event, awardList in awardData.items():
        eventData = event.split("|")
        awards.append(
            {"event": {"name": eventData[0], "code": eventData[1]}, "awards": awardList})

    for event in awards:
        print(event["event"]["name"])
        for award in event["awards"]:
            print(award)
    return awards

def get_id(noteYes):
    r = requests.get(f"https://www.robotevents.com/teams/VRC/210Z")
    soup = BeautifulSoup(r.text, "html.parser")
    teamId = api_get("teams", params={"number": noteYes})['data'][0]['id'] 
    return teamId



@views.route('/', methods = ["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short", category = "error")
        team = get_id(note)
        return render_template(
        "home.html",
        user = current_user,
        awards = get_awards(team),
        skillsRank = get_skills_score(note),
        robotName = get_robot_name(note),
        gradeLevel = get_grade_level(note),
        location = get_location(note),
        program = get_program(note),
        name = note
        )

    else:
        note = request.form.get("note")
        new_note = Note(data = note, user_id = current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added!", category = "success")
        return render_template("home.html", user = current_user)



@views.route("/delete-note", methods = ["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

