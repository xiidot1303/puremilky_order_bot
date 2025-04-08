from app.services import *
from app.models import Feedback


async def create_feedback(comment, bot_user=None, order=None) -> Feedback:
    feedback = Feedback(
        comment=comment,
        bot_user=bot_user,
        order=order
    )
    await feedback.asave()
    return Feedback