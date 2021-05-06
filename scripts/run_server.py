"""
Script that starts web server
"""


import fastapi

import net.routes.users

app = fastapi.FastAPI()

app.include_router(net.routes.users.router)
