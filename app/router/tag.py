from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Any, List

from app.schema.tag import (
    TagCreate,
    TagUpdate,
    Tag
)
from app.router import deps
from app.crud import (
    crud_tag
)

tag_router = APIRouter(prefix="/tag")


@tag_router.get('/', status_code=200, response_model=List[Tag])
async def get_tags(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    ) -> Any:

    tags = crud_tag.tag.get_multi(db, skip=skip, limit=limit)

    return tags


@tag_router.get('/{tag_id}', status_code=200, response_model=Tag)
async def get_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: int
    ) -> Any:

    tag = crud_tag.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=400,
            detail=f"The tag with id {tag_id} does not exists in the system.",
        )

    return tag


@tag_router.post('/', status_code=201, response_model=Tag)
async def create_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: TagCreate,
    ) -> Any:

    tag = crud_tag.tag.get_by_name(db, name=tag_in.name)
    if tag:
        raise HTTPException(
            status_code=400,
            detail="The tag with this name already exists in the system.",
        )

    tag = crud_tag.tag.create(db, obj_in=tag_in)
    return tag


@tag_router.put('/{tag_id}', status_code=200, response_model=Tag)
async def update_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_in: TagUpdate,
    tag_id: int
    ) -> Any:

    tag = crud_tag.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=400,
            detail=f"The tag with id {tag_id} does not exists in the system.",
        )

    tag = crud_tag.tag.update(db, db_obj=tag, obj_in=tag_in)
    return tag


@tag_router.delete('/{tag_id}', status_code=200, response_model=Tag)
async def delete_tag(
    *,
    db: Session = Depends(deps.get_db),
    tag_id: int
    ) -> Any:

    tag = crud_tag.tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=400,
            detail=f"The tag with id {tag_id} does not exists in the system.",
        )

    crud_tag.tag.remove(db, id=tag_id)
    return tag
