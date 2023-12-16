

from fastapi import HTTPException, status


def bad_exception400(msg:str)-> HTTPException:
    return HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )

def unauthorized_exception401(msg: str, headers:str | None)-> HTTPException:
    return HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers=headers,
    )

def notfound_exception404(msg: str)-> HTTPException:
    return HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail=msg,
    )
