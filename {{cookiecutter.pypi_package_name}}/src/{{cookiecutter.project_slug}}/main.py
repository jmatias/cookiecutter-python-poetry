import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from {{cookiecutter.project_slug}} import version_str
from {{cookiecutter.project_slug}}.config import swagger_servers, cors_origins, FASTAPI_ROOT_PATH
from {{cookiecutter.project_slug}}.controllers import activity, fruits, vegetables

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.debug("Starting up the FastAPI application...")
    yield
    logger.debug("Tearing down the FastAPI application...")


description = """
### Evidence Vault API
"""
app = FastAPI(
    lifespan=lifespan,
    title="FastAPI Example with AWS Lambda",
    description=description,
    swagger_ui_parameters={"tryItOutEnabled": True, "operationsSorter": "method"},
    version=version_str,
    root_path=FASTAPI_ROOT_PATH,
    root_path_in_servers=False,
    servers=swagger_servers,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(activity.router, prefix="/activities")
app.include_router(fruits.router, prefix="/fruits")
app.include_router(vegetables.router, prefix="/vegetables")


@app.get("/", operation_id="hello")
def hello_world():
    return {"message": "Hello, world!"}


@app.post("/webhook", operation_id="webhook")
def webhook(event: dict):
    print("Webhook event received:", event)
    return {"status": "success", "event": event}


#################################################
######### FastAPI to AWS Lambda Adapter #########
#################################################


def handler(event, context):
    print("Event: ", event)
    # EventBridge events have "detail-type" and "detail"
    if "detail-type" in event and "detail" in event:
        # handle event
        print("Hello from Lambda! Event: ", event)
        return {"statusCode": 200, "body": "Hello from Lambda!", event: event}
    else:
        return Mangum(app, lifespan="on")(event, context)
