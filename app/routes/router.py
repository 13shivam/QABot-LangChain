import json
import uuid
from typing import Any

from fastapi import APIRouter, Path

from app.config.producer_config import producer
from app.schemas.file_upload_request import FileUploadRequest
from app.schemas.file_upload_response import FileUploadResponse
from app.service.retrieval_iqa import retrieve_task

v1_router = APIRouter(prefix="/v1")


@v1_router.post(
    "/upload",
    summary="Upload file and questions",
    responses={
        201: {"description": "success"},
    },
)
async def upload_file_w_questions(request: FileUploadRequest) -> FileUploadResponse:
    task_id = str(uuid.uuid4())
    try:
        data_to_push = {
            'document_path': request.document_file_path,
            'question_path': request.question_file_path,
            'task_id': task_id
        }
        json_data = json.dumps(data_to_push)
        producer.produce("demollm", value=json_data)
        producer.flush()
        print(f"Successfully uploaded Doc and Questionnaire: {request}")
        return FileUploadResponse(task_id=task_id, status=200)

    except Exception as e:
        return FileUploadResponse(task_id="unable to upload file", status=500)


@v1_router.get(
    "/task/{task_id}",
    summary="Get",
    responses={
        200: {"description": "success"},
        404: {"description": "failed"},
    },
)
async def query(task_id: str = Path(..., title="The ID of the task")) -> Any:
    x = retrieve_task(task_id)
    return x
