from fastapi import Request, HTTPException, status


async def require_auth(request: Request):
    # TODO: Replace with real session/JWT check
    if not request.session.get("user"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")





