from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.routers import clients
from app import crud
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM 專案管理系統")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(clients.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, search: str = None, db: Session = Depends(get_db)):
    clients_list = crud.get_clients(db, search=search)
    stats = crud.get_statistics(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "clients": clients_list,
            "stats": stats,
            "search": search or ""
        }
    )

@app.get("/client/new", response_class=HTMLResponse)
async def new_client_form(request: Request):
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": None, "action": "/api/clients/", "method": "POST"}
    )

@app.get("/client/{client_id}/edit", response_class=HTMLResponse)
async def edit_client_form(request: Request, client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse(
        "client_form.html",
        {"request": request, "client": client, "action": f"/api/clients/{client_id}", "method": "PUT"}
    )

@app.get("/import", response_class=HTMLResponse)
async def import_page(request: Request):
    return templates.TemplateResponse("import_csv.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
