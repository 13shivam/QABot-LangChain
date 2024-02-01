import json

from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from app.schemas.answer_response import AnswerResponse
from app.schemas.file_upload_request import FileUploadRequest
from app.utils.dir import get_project_root_output_dir, write_result_file_for_task
from app.utils.parser import load_pdf, read_json


class RetrievalIQA:

    def __init__(self, file_path: str):
        self.vectordb = None
        self.file_path = file_path

    def retrieval_qa_chain(self):
        return RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type="stuff",
            retriever=self.vectordb.as_retriever()
        )

    @staticmethod
    def embeddings(texts: list[Document]):
        embeddings = OpenAIEmbeddings()
        return Chroma.from_documents(texts, embeddings)

    @staticmethod
    def split_strings(documents: TextLoader):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=0)
        return text_splitter.split_documents(documents)


def do_the_thing(request: FileUploadRequest, task_id: str):
    loaded_file_path = load_pdf(request.document_file_path)
    json_questions = read_json(request.question_file_path)
    # create retrieval QA
    rq = RetrievalIQA(loaded_file_path)
    loaded_document = TextLoader(loaded_file_path).load()
    rq.vectordb = rq.embeddings(rq.split_strings(loaded_document))
    chain_ready = rq.retrieval_qa_chain()

    results = []

    for question_entry in json_questions:
        question = question_entry.get("question")
        result = chain_ready.invoke(question)
        results.append(AnswerResponse(question=question, answer=result.get("result")))

    return task_id, write_result_file_for_task(task_id, loaded_file_path, results)


def retrieve_task(task_id: str):
    resource_path = get_project_root_output_dir()
    result = []
    try:
        with open(resource_path + task_id + ".json", 'r') as json_file:
            data_dict_list = json.load(json_file)
    except FileNotFoundError:
        # TODO
        return "Job for indexing the document is still in progress or task Id not created."
    except Exception as e:
        return f"An error occurred: {e}"

    result = [AnswerResponse(**entry) for entry in data_dict_list]
    return result
