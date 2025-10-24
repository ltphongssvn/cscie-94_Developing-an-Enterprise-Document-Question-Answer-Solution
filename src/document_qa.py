# src/document_qa.py
# Full path: /src/document_qa.py

import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.document_loader import MultiFormatDocumentLoader


class DocumentQASystem:
    """Enterprise Document Question-Answer Solution using Azure OpenAI and Cognitive Search."""

    def __init__(self):
        """Initialize the QA system with Azure configurations."""
        load_dotenv()

        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.qa_chain = None
        self.document_loader = MultiFormatDocumentLoader()

    def initialize_embeddings(self):
        """Initialize Azure OpenAI embeddings."""
        self.embeddings = AzureOpenAIEmbeddings(
            azure_endpoint=self.azure_endpoint,
            api_key=self.azure_api_key,
            api_version=self.api_version,
            azure_deployment=self.embedding_deployment,
        )
        print("✓ Embeddings initialized")

    def load_documents(self, data_dir="data"):
        """Load documents from directory."""
        self.document_loader = MultiFormatDocumentLoader(data_dir)
        documents = self.document_loader.load_all()

        file_counts = self.document_loader.get_file_count()
        print(f"✓ Loaded {len(documents)} document pages")
        print(f"  File types: {file_counts}")

        return documents

    def split_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        """Split documents into chunks."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Split into {len(chunks)} chunks")
        return chunks

    def initialize_vector_store(self, chunks):
        """Initialize Azure Cognitive Search vector store and upsert chunks."""
        self.vector_store = AzureSearch(
            azure_search_endpoint=self.search_endpoint,
            azure_search_key=self.search_key,
            index_name=self.index_name,
            embedding_function=self.embeddings.embed_query,
        )

        self.vector_store.add_documents(documents=chunks)
        print(f"✓ Upserted {len(chunks)} chunks to Azure Search")

    def initialize_llm(self):
        """Initialize Azure OpenAI LLM."""
        self.llm = AzureChatOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.azure_api_key,
            api_version=self.api_version,
            azure_deployment=self.deployment_name,
            temperature=0,
        )
        print("✓ LLM initialized")

    def create_qa_chain(self, top_k=3):
        """Create retrieval chain."""
        retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k})

        prompt = ChatPromptTemplate.from_template(
            """Answer based on context:

Context: {context}

Question: {input}"""
        )

        document_chain = create_stuff_documents_chain(self.llm, prompt)
        self.qa_chain = create_retrieval_chain(retriever, document_chain)
        print("✓ QA chain created")

    def query(self, question):
        """Query the system and return answer."""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Run setup first.")

        result = self.qa_chain.invoke({"input": question})
        return {
            "result": result["answer"],
            "source_documents": result.get("context", []),
        }

    def setup(self, data_dir="data"):
        """Complete setup process."""
        print("Setting up Document QA System...")

        self.initialize_embeddings()
        documents = self.load_documents(data_dir)
        chunks = self.split_documents(documents)
        self.initialize_vector_store(chunks)
        self.initialize_llm()
        self.create_qa_chain()

        print("\n✓ System ready for queries!")


def main():
    """Main execution function."""
    qa_system = DocumentQASystem()
    qa_system.setup()

    queries = [
        "What are the main destinations in this travel itinerary?",
        "What is included in the package?",
        "What are the accommodation details?",
    ]

    for question in queries:
        result = qa_system.query(question)
        print(f"\nQuestion: {question}")
        print(f"Answer: {result['result']}")
        print("-" * 80)


if __name__ == "__main__":
    main()
