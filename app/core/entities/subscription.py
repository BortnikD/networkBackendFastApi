from dataclasses import dataclass


@dataclass
class Subscription:
    id: int
    follower_id: int
    followed_user_id: int
