from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.usuario import Usuario, UsuarioCreate, UsuarioOut 
from app.db.db import get_db  

router = APIRouter()

@router.post("/usuario/", response_model=UsuarioOut)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    db_usuario = Usuario(nome=usuario.nome, email=usuario.email, senha_hash=usuario.senha)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.get("/usuario/{usuario_id}", response_model=UsuarioOut)
def read_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario
