from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional

def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None):
    query = db.query(models.Client)
    if search:
        query = query.filter(
            (models.Client.client_name.ilike(f"%{search}%")) |
            (models.Client.project_name.ilike(f"%{search}%"))
        )
    # 排序：最後修改時間新到舊（updated_at 優先，若為 None 則用 created_at）
    query = query.order_by(
        models.Client.updated_at.desc().nullslast(),
        models.Client.created_at.desc()
    )
    return query.offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client: schemas.ClientUpdate):
    db_client = get_client(db, client_id)
    if db_client:
        update_data = client.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client

def get_statistics(db: Session):
    total_clients = db.query(models.Client).count()
    total_cost = db.query(models.Client).with_entities(
        models.Client.project_cost
    ).all()
    total_amount = sum([c[0] for c in total_cost]) if total_cost else 0
    avg_amount = total_amount / total_clients if total_clients > 0 else 0
    
    return {
        "total_clients": total_clients,
        "total_amount": total_amount,
        "average_amount": int(avg_amount)
    }
