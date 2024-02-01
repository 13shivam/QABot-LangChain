import asyncio
import json

import uvicorn
from aiokafka import AIOKafkaConsumer
from dotenv import load_dotenv
from fastapi import FastAPI

from app.config.base_config import dotenv_path
from app.config.consumer_config import consumer_config
from app.schemas.file_upload_request import FileUploadRequest
from app.service.retrieval_iqa import do_the_thing

load_dotenv(dotenv_path)

worker_app = FastAPI()


async def consume_messages():
    consumer = AIOKafkaConsumer(
        consumer_config.topic,
        bootstrap_servers=consumer_config.bootstrap_servers,
    )

    await consumer.start()
    print(f"LLM consumer started !!")
    try:
        async for msg in consumer:
            message_data = json.loads(msg.value.decode('utf-8'))
            print(f"Received message: {message_data}")
            f = FileUploadRequest(document_file_path=message_data['document_path'],
                                  question_file_path=message_data['question_path'])
            do_the_thing(f, message_data['task_id'])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    finally:
        await consumer.stop()


@worker_app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_messages())


if __name__ == "__worker_main__":
    uvicorn.run(worker_app, host="0.0.0.0", log_level="info", port=8001)
