from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.dependencies import D
from src.services.cases.routes import case_router
from src.services.members.routes import team_member_router
from src.services.security.routes import security_router
from src.services.teams.routes import team_router
from src.services.users.routes import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_storage = D.session_storage()

    #####  ПОКА НЕ ИСПОЛЬЗУЕТСЯ

    # is_exists_bucket = s3.create_bucket(config.settings.MINIO_BUCKET_NAME)
    # if not is_exists_bucket:
    #     await s3.make_bucket(config.settings.MINIO_AVATAR_BUCKET_NAME)
    # await s3_client.create_bucket(config.settings.MINIO_BUCKET_NAME)

    #####

    mongo = D.mongo()
    await mongo.init()
    await session_storage.info()
    yield
    await session_storage.aclose()


app = FastAPI(lifespan=lifespan)


##### НАСТРОИТЬ ПОД КОНКРЕТНЫЕ ИСТОЧНИКИ (вынести в конфиг)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#####

app.include_router(security_router)
app.include_router(user_router)
team_router.include_router(team_member_router)
app.include_router(team_router)
app.include_router(case_router)
