from fastapi import FastAPI, BackgroundTasks
from pms.routers.user_routes import api_router as pms_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from pms.database.db_models.user_orm import database
import pika, asyncio, threading
from pms.listeners.auth.auth_listener import auth_listener


def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="auth_to_pms")
    channel.basic_consume(
        queue="auth_to_pms", on_message_callback=auth_listener, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
    # connection.process_data_events(time_limit=None)


# def start_message_consumer(background_tasks: BackgroundTasks):
#     background_tasks.add_task(consume_messages)


def get_app():
    app = FastAPI(
        title="KTutors People management Service Routes",
        description=(
            "This routes helps create user profile"
            "for all other services of KTutors Project\t"
        ),
        version="0.0.1",
    )

    app.include_router(pms_router)

    @app.on_event("startup")
    async def startup():
        await database.connect()
        # start_message_consumer(background_tasks=background_tasks)
        background_thread = threading.Thread(target=consume_messages)
        background_thread.daemon = True
        background_thread.start()
        # loop = asyncio.get_running_loop()
        # task = loop.create_task(consume_messages())
        # await task
        print("db connected")

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
        print("db disconnected")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
