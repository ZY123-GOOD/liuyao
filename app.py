from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

BASE_DIR = os.path.dirname(__file__)
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# 挂载静态文件
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request):
    form = await request.form()
    question = form["question"]
    heads = form["coins"].split(",")
    coins = map_heads_to_lines(heads)

    # 创建卦（示例）
    # divination = Divination(question=question, coins=coins)
    # divination.initialize()
    # result = run(divination)

    result = "示例结果"  # 测试用

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result
    })

def map_heads_to_lines(heads):
    mapping = {0: 8, 1: 7, 2: 9, 3: 6}
    return [mapping[int(x)] for x in heads]