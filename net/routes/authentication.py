"""
Module with authentication routes that fastapi-users doesn't provide
"""

import fastapi
import fastapi_users.router.common
import pydantic
import sqlalchemy.orm.session

import net.backend
import net.dependencies
import net.models

router = fastapi.APIRouter()


class Send2FACodePostRequest(pydantic.BaseModel):
    """
    Model for POST send_2FA_code request
    """

    username: str
    password: str


class Confirm2FACodePostRequest(Send2FACodePostRequest):
    """
    Model for POST confirm_2FA_code request
    """

    code: str


@router.post("/send_2FA_code", response_model=str, status_code=201)
async def send_2FA_code(
        payload: Send2FACodePostRequest,
        session: sqlalchemy.orm.session.Session = fastapi.Depends(net.dependencies.yield_mysql_session)):
    """
    Send 2FA code
    """

    # Get password hash
    user = await net.models.user_db.authenticate(payload)

    if user is None or not user.is_active:

        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=fastapi_users.router.common.ErrorCode.LOGIN_BAD_CREDENTIALS,
        )

    time_base_one_time_password = net.backend.generate_time_based_one_time_password(
        secret=user.uniquifier
    )

    # Simulate emailing token to user :P
    print(time_base_one_time_password)

    return "OK"


@router.post("/confirm_2FA_code", status_code=201)
async def confirm_2FA_code(
        payload: Confirm2FACodePostRequest,
        response: fastapi.Response,
        session: sqlalchemy.orm.session.Session = fastapi.Depends(net.dependencies.yield_mysql_session)
):
    """
    Send 2FA code
    """

    # Get password hash
    user = await net.models.user_db.authenticate(payload)

    if user is None or not user.is_active:

        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=fastapi_users.router.common.ErrorCode.LOGIN_BAD_CREDENTIALS,
        )

    time_base_one_time_password = net.backend.generate_time_based_one_time_password(
        secret=user.uniquifier
    )

    if time_base_one_time_password == payload.code:

        return await net.models.fastapi_users_app.authenticator.backends[0].get_login_response(user, response)

    else:

        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=fastapi_users.router.common.ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
