

from fastapi import HTTPException, status


def bad_exception400(msg:str)-> HTTPException:
    return HTTPException(
        status_code= status.HTTP_400_BAD_REQUEST,
        detail=msg,
    )
