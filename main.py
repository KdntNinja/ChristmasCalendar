import json
import os
from datetime import datetime
from random import choice

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates


class ChristmasApp:
    def __init__(self):
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="templates")
        self.christmas_messages = self.load_messages()
        with open("christmas_facts.json", "r") as file:
            self.christmas_facts = json.load(file)
        self.setup_routes()

    def setup_routes(self):
        self.app.get("/", response_class=HTMLResponse)(self.root)
        self.app.get("/time_until_christmas")(self.time_until_christmas)
        self.app.get("/random_christmas_fact")(self.random_christmas_fact)
        self.app.get("/milestone_messages")(self.milestone_messages)
        self.app.post("/add_message")(self.add_message)

    async def root(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    @staticmethod
    async def time_until_christmas():
        now = datetime.now()
        christmas = datetime(now.year, 12, 25)
        if now > christmas:
            christmas = datetime(now.year + 1, 12, 25)
        time_until = christmas - now
        days, seconds = time_until.days, time_until.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        formatted_time_until = f"{days}d {hours}h {minutes}m {seconds}s"
        return {"time_until_christmas": formatted_time_until}

    async def random_christmas_fact(self):
        fact = choice(self.christmas_facts)
        return {"fact": fact}

    @staticmethod
    async def milestone_messages():
        milestone_messages = {
            "10": "Only 10 days left until Christmas! 🎄",
            "5": "Just 5 days to go! 🎅",
            "2": "Only 2 days left! Get ready! 🎁",
            "1": "Tomorrow is Christmas! 🎉",
            "0": "Merry Christmas! 🎄🎅🎁"
        }
        return JSONResponse(content=milestone_messages)

    async def add_message(self, request: Request):
        data = await request.json()
        message = data.get("message")
        self.christmas_messages.append(message)
        self.save_messages()
        return JSONResponse(content={"message": message})

    def save_messages(self):
        with open("christmas_messages.json", "w") as file:
            json.dump(self.christmas_messages, file)

    @staticmethod
    def load_messages():
        if os.path.exists("christmas_messages.json"):
            with open("christmas_messages.json", "r") as file:
                return json.load(file)
        return []


christmas_app = ChristmasApp()
app = christmas_app.app
