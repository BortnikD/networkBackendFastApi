from fastapi import Depends

from app.core.services.subscription_servise import SubscriptionService
from app.adapters.repositories.subscription_repository import SubscriptionRepository
from app.adapters.api.dependencies.db import get_db


def get_user_service(db=Depends(get_db)) -> SubscriptionService:
    subscription = SubscriptionRepository(db)
    return SubscriptionService(subscription)