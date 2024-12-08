import random
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("christmas_facts.json", "r") as file:
    christmas_facts = json.load(file)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/time_until_christmas")
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


@app.get("/random_christmas_fact")
async def random_christmas_fact():
    fact = random.choice(christmas_facts)
    return {"fact": fact}
