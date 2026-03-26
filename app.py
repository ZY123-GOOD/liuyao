from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from engine.divination import Divination
from engine.pipeline import run

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(

        request,

        "index.html",

        {

            "request":request

        }

    )


@app.post("/analyze")
async def analyze(request: Request):

    form = await request.form()

    question = form["question"]

    heads = form["coins"].split(",")

    coins = map_heads_to_lines(heads)

    divination = Divination(

        question=question,

        coins=coins

    )

    divination.initialize()

    result = run(divination)

    return templates.TemplateResponse(

        request,

        "index.html",

        {

            "request":request,

            "divination":divination.ui_data(),

            "result":result

        }

    )


def map_heads_to_lines(heads):

    mapping = {

        0:8,

        1:7,

        2:9,

        3:6

    }

    return [

        mapping[int(x)]

        for x in heads

    ]