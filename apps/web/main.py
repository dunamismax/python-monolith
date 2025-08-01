from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fasthx import Jinja

app = FastAPI(title="Python Monolith Web App")

app.mount("/static", StaticFiles(directory="apps/web/static"), name="static")

templates = Jinja2Templates(directory="apps/web/templates")
jinja = Jinja(templates)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/clicked")
@jinja.hx_template("clicked.html")
async def clicked():
    return {"message": "Hello from HTMX! The button was clicked successfully."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)