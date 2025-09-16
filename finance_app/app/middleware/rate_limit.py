from time import time
from typing import Dict, List
from fastapi import Request, HTTPException, status

# Simple in-memory limiter (replace with Redis in production)
_ip_bucket: Dict[str, List[float]] = {}


def _prune_timestamps(timestamps: List[float], window_seconds: int) -> List[float]:
    threshold = time() - window_seconds
    return [t for t in timestamps if t >= threshold]


def rate_limit_middleware(max_requests_per_minute: int = 100):
    window = 60

    async def _middleware(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        timestamps = _ip_bucket.get(client_ip, [])
        timestamps = _prune_timestamps(timestamps, window)
        if len(timestamps) >= max_requests_per_minute:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        timestamps.append(time())
        _ip_bucket[client_ip] = timestamps
        return await call_next(request)

    return _middleware


