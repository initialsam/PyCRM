from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from typing import List
import pandas as pd
import io

router = APIRouter(prefix="/api/clients", tags=["clients"])

@router.get("/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, search: str = None, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, skip=skip, limit=limit, search=search)
    return clients

@router.get("/statistics")
def read_statistics(db: Session = Depends(get_db)):
    return crud.get_statistics(db)

@router.get("/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="客戶不存在")
    return db_client

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)

@router.put("/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    db_client = crud.update_client(db, client_id=client_id, client=client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="客戶不存在")
    return db_client

@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.delete_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="客戶不存在")
    return {"message": "刪除成功"}

@router.post("/import-csv")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="請上傳 CSV 檔案")
    
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    imported = 0
    for _, row in df.iterrows():
        client = schemas.ClientCreate(
            client_name=row['客戶名稱'],
            project_name=row['專案名稱'],
            email=row['email'],
            project_cost=int(row['專案費用'])
        )
        crud.create_client(db, client)
        imported += 1
    
    return {"message": f"成功匯入 {imported} 筆資料"}
