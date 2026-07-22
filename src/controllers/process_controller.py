from controllers.base_controller import BaseController
from controllers.project_controller import ProjectController
import os
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from enums import ProcessingEnum


class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extention(self, file_id: str):
        return os.path.splitext(file_id)[-1]

    def get_file_load(self, file_id: str):
        try:
            file_path = os.path.join(self.project_path, file_id)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"file with id {file_id} not found")

            file_ext = self.get_file_extention(file_id=file_id)

            if file_ext == ProcessingEnum.TXT.value:
                return TextLoader(file_path=file_path, encoding="utf-8")

            if file_ext == ProcessingEnum.PDF.value:
                return PyMuPDF4LLMLoader(file_path=file_path)

            return None
        except Exception:
            raise

    def get_file_content(self, file_id: str):
        loader = self.get_file_load(file_id=file_id)
        return loader.load()

    def process_file_content(
        self, file_content: list, chunk_size: int = 100, chunk_overlap: int = 20
    ):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
        )

        file_context_texts = [rec.page_content for rec in file_content]
        file_context_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(
            file_context_texts, metadatas=file_context_metadata
        )

        return chunks
