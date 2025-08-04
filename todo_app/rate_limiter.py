from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

def get_rate_limit_key(request: Request):
    """Get the key for rate limiting - using IP address"""
    return get_remote_address(request)

limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=["50/hour"],
    headers_enabled=False  
)

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors"""
    return {
        "error": "Rate limit exceeded", 
        "detail": str(exc.detail),
        "retry_after": exc.retry_after
    }