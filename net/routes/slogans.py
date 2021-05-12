"""
Slogans endpoints
"""

import fastapi

import net.globals


router = fastapi.APIRouter()


@router.get("/slogans", response_model=list[str])
def get_slogans():
    """
    Get slogans
    """

    return ["first slogan " + net.globals.CONFIG["environment"], "second slogan " + net.globals.CONFIG["environment"]]
