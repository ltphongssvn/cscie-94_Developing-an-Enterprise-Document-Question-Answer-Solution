# tests/test_document_qa.py
# Full path: /tests/test_document_qa.py

import pytest
from unittest.mock import Mock, patch
from src.document_qa import DocumentQASystem


class TestDocumentQASystem:
    """Test cases for DocumentQASystem."""

    @patch("src.document_qa.load_dotenv")
    def test_initialization(self, mock_load_dotenv):
        """Test system initialization."""
        qa_system = DocumentQASystem()
        assert qa_system.embeddings is None
        assert qa_system.vector_store is None
        assert qa_system.llm is None
        assert qa_system.qa_chain is None

    @patch("src.document_qa.AzureOpenAIEmbeddings")
    @patch("src.document_qa.load_dotenv")
    def test_initialize_embeddings(self, mock_load_dotenv, mock_embeddings):
        """Test embeddings initialization."""
        qa_system = DocumentQASystem()
        qa_system.initialize_embeddings()
        assert mock_embeddings.called

    @patch("src.document_qa.DirectoryLoader")
    @patch("src.document_qa.load_dotenv")
    def test_load_documents(self, mock_load_dotenv, mock_loader):
        """Test document loading."""
        mock_loader.return_value.load.return_value = [Mock(), Mock()]
        qa_system = DocumentQASystem()
        documents = qa_system.load_documents()
        assert len(documents) == 2

    @patch("src.document_qa.RecursiveCharacterTextSplitter")
    @patch("src.document_qa.load_dotenv")
    def test_split_documents(self, mock_load_dotenv, mock_splitter):
        """Test document splitting."""
        mock_docs = [Mock(), Mock()]
        mock_splitter.return_value.split_documents.return_value = [
            Mock(),
            Mock(),
            Mock(),
        ]
        qa_system = DocumentQASystem()
        chunks = qa_system.split_documents(mock_docs)
        assert len(chunks) == 3

    @patch("src.document_qa.load_dotenv")
    def test_query_without_setup(self, mock_load_dotenv):
        """Test query fails without setup."""
        qa_system = DocumentQASystem()
        with pytest.raises(ValueError):
            qa_system.query("test question")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
