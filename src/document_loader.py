# src/document_loader.py
# Full path: /src/document_loader.py

from pathlib import Path
from typing import List
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)


class MultiFormatDocumentLoader:
    """Load documents from multiple formats."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.supported_formats = {".pdf", ".txt", ".docx", ".doc"}

    def load_all(self) -> List[Document]:
        """Load all supported documents from directory."""
        documents = []

        for file_path in self.data_dir.rglob("*"):
            if file_path.suffix.lower() in self.supported_formats:
                docs = self._load_single_file(file_path)
                documents.extend(docs)

        return documents

    def _load_single_file(self, file_path: Path) -> List[Document]:
        """Load a single file based on extension."""
        suffix = file_path.suffix.lower()

        try:
            if suffix == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif suffix == ".txt":
                loader = TextLoader(str(file_path))
            elif suffix in [".docx", ".doc"]:
                loader = UnstructuredWordDocumentLoader(str(file_path))
            else:
                return []

            return loader.load()

        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return []

    def get_file_count(self) -> dict:
        """Get count of files by type."""
        counts = {fmt: 0 for fmt in self.supported_formats}

        for file_path in self.data_dir.rglob("*"):
            suffix = file_path.suffix.lower()
            if suffix in self.supported_formats:
                counts[suffix] += 1

        return counts
