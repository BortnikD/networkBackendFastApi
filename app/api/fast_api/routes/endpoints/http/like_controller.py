from typing import Annotated
from fastapi import APIRouter, Query, Depends, HTTPException

from app.domain.dto.pagination import LikePagination, PaginatedResponse
from app.domain.dto.like import LikeCreate
from app.domain.entities.like import Like
from app.domain.entities.user import User
from app.domain.exceptions.like import (
    AlreadyLikedPost,
    LikeDoesNotExist,
    LikeDeleteError,
)

from app.services.core_services.like_service import LikeService
from app.dependencies.services.like import get_like_service
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix='/likes')


@router.get('/{post_id}')
async def read_likes(
        post_id: int,
        pagination: Annotated[LikePagination, Query()],
        like_service: LikeService = Depends(get_like_service)
        ) -> PaginatedResponse:
    """Получение списка лайков по ID поста."""
    return await like_service.get_all_by_post_id(post_id, pagination.offset, pagination.limit)


@router.post('/')
async def create_like(
        like: LikeCreate,
        current_user: User = Depends(get_current_active_user),
        like_service: LikeService = Depends(get_like_service)
        ) -> Like:
    """Создание лайка для поста."""
    try:
        return await like_service.save(like.post_id, current_user.id)
    except AlreadyLikedPost as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.delete('/{post_id}')
async def delete_like(
        post_id: int,
        current_user: User = Depends(get_current_active_user),
        like_service: LikeService = Depends(get_like_service)
        ) -> None:
    """Удаление лайка с поста."""
    try:
        return await like_service.delete(post_id, current_user.id)
    except LikeDoesNotExist as e:
        raise HTTPException(status_code=404, detail=e.message)
    except LikeDeleteError as e:
        raise HTTPException(status_code=500, detail=e.message)
