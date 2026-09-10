from collections import defaultdict, deque
from datetime import datetime, timedelta
from typing import Deque, Dict, Tuple

from fastapi import HTTPException, Request, status

from .config import settings

_per_minute: Dict[str, Deque[datetime]] = defaultdict(deque)
_per_hour: Dict[str, Deque[datetime]] = defaultdict(deque)


def _prune(queue: Deque[datetime], window: timedelta) -> None:
    cutoff = datetime.utcnow() - window
    while queue and queue[0] < cutoff:
        queue.popleft()


async def rate_limiter(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.utcnow()

    minute_queue = _per_minute[client_ip]
    hour_queue = _per_hour[client_ip]

    _prune(minute_queue, timedelta(minutes=1))
    _prune(hour_queue, timedelta(hours=1))

    if len(minute_queue) >= settings.rate_limit_per_minute or len(
        hour_queue
    ) >= settings.rate_limit_per_hour:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )

    minute_queue.append(now)
    hour_queue.append(now)
