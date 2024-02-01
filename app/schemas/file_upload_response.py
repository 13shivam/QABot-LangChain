from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    status: int
    task_id: str

    def __str__(self):
        return f"Status: {self.status}, Task Id: {self.task_id}"
