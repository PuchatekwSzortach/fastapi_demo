"""
Tasks to run most common processes
"""

import invoke


@invoke.task
def web(context):
    """
    Run web server
    """

    command = "uvicorn net.applications:get_fastapi_app --host 0.0.0.0 --reload"
    context.run(command, echo=True)
