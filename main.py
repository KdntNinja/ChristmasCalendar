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
        self.gift_list = self.load_gifts()
        with open("christmas_facts.json", "r") as file:
            self.christmas_facts = json.load(file)
        self.setup_routes()

    def setup_routes(self):
        self.app.get("/", response_class=HTMLResponse)(self.root)
        self.app.get("/time_until_christmas")(self.time_until_christmas)
        self.app.get("/random_christmas_fact")(self.random_christmas_fact)
        self.app.get("/milestone_messages")(self.milestone_messages)
        self.app.post("/add_message")(self.add_message)
        self.app.post("/add_gift")(self.add_gift)

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

    async def add_gift(self, request: Request):
        data = await request.json()
        gift = data.get("gift")
        self.gift_list.append(gift)
        self.save_gifts()
        return JSONResponse(content={"gift": gift})

    def save_messages(self):
        with open("christmas_messages.json", "w") as file:
            json.dump(self.christmas_messages, file)

    def save_gifts(self):
        with open("gift_list.json", "w") as file:
            json.dump(self.gift_list, file)

    @staticmethod
    def load_messages():
        if os.path.exists("christmas_messages.json"):
            with open("christmas_messages.json", "r") as file:
                return json.load(file)
        return []

    @staticmethod
    def load_gifts():
        if os.path.exists("gift_list.json"):
            with open("gift_list.json", "r") as file:
                return json.load(file)
        return []


christmas_app = ChristmasApp()
app = christmas_app.app
