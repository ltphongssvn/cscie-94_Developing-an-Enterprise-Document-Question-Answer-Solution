# src/document_qa.py
# Full path: /src/document_qa.py

import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import RetrievalQA


class DocumentQASystem:
    """Enterprise Document Question-Answer Solution using Azure OpenAI and Cognitive Search."""

    def __init__(self):
        """Initialize the QA system with Azure configurations."""
        load_dotenv()

        # Azure OpenAI Configuration
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

        # Azure Search Configuration
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

        # Initialize components
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.qa_chain = None

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
        loader = DirectoryLoader(data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
        print(f"✓ Loaded {len(documents)} documents")
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

        # Upsert documents
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
        """Create RetrievalQA chain."""
        retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k})

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        print("✓ QA chain created")

    def query(self, question):
        """Query the system and return answer."""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized. Run setup first.")

        result = self.qa_chain({"query": question})
        return result

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
    # Initialize system
    qa_system = DocumentQASystem()

    # Setup (load and index documents)
    qa_system.setup()

    # Example query
    question = "What are the main features of the travel itinerary?"
    result = qa_system.query(question)

    print(f"\nQuestion: {question}")
    print(f"Answer: {result['result']}")


if __name__ == "__main__":
    main()
