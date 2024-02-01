from pydantic import BaseModel


class FileUploadRequest(BaseModel):
    document_file_path: str
    question_file_path: str

    def __str__(self):
        return f"Document Path: {self.document_file_path}, Question Path: {self.question_file_path}"
