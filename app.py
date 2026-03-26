from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from engine.divination import Divination
from engine.pipeline import run

app = FastAPI()


# import os
# BASE_DIR = os.path.dirname(__file__)  # app.py 所在目录
# templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):

    return templates.TemplateResponse(
    "index.html",
    {"request":request}
    )


@app.post("/analyze")
async def analyze(request: Request):

    form = await request.form()

    question = form["question"]

    # coins = [

    #     int(x)

    #     for x in form["coins"].split(",")

    # ]
    heads = form["coins"].split(",")

    coins = map_heads_to_lines(heads)

    # 创建卦

    divination = Divination(

        question=question,

        coins=coins

    )

    divination.initialize()

    # 运行推理

    result = run(divination)

    return templates.TemplateResponse(

        "index.html",

        {

            "request":request,

            "divination":divination,

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