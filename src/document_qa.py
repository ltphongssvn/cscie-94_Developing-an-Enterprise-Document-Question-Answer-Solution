# Full path: /src/document_qa.py
import os
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.chains import RetrievalQA

from src.document_loader import MultiFormatDocumentLoader


class DocumentQASystem:
    """Enterprise Document Question-Answer Solution using Azure OpenAI and Cognitive Search."""

    def __init__(self):
        """Initialize the QA system with Azure configurations."""
        load_dotenv()

        # Azure OpenAI Configuration
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.embedding_deployment_name = os.getenv(
            "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
        )

        # Azure Cognitive Search Configuration
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.search_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")

        # Initialize components
        self.embeddings = None
        self.vector_store = None
        self.llm = None
        self.qa_chain = None

    def initialize_embeddings(self):
        """Initialize Azure OpenAI embeddings."""
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=self.embedding_deployment_name,
            azure_endpoint=self.openai_endpoint,
            api_key=self.openai_api_key,
            api_version=self.openai_api_version,
        )
        print("✓ Embeddings initialized")

    def load_documents(self, directory="data"):
        """Load documents from the specified directory."""
        loader = MultiFormatDocumentLoader(directory)
        documents = loader.load_all()

        print(f"✓ Loaded {len(documents)} document pages")
        print(f"  File types: {loader.get_file_count()}")

        return documents

    def split_documents(self, documents, chunk_size=1000, chunk_overlap=200):
        """Split documents into chunks for processing."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Split into {len(chunks)} chunks")
        return chunks

    def initialize_vector_store(self, chunks):
        """Initialize Azure Cognitive Search as vector store."""
        self.vector_store = AzureSearch(
            azure_search_endpoint=self.search_endpoint,
            azure_search_key=self.search_api_key,
            index_name=self.search_index_name,
            embedding_function=self.embeddings.embed_query,
        )

        # Add documents to vector store
        self.vector_store.add_documents(chunks)
        print(f"✓ Upserted {len(chunks)} chunks to Azure Search")

    def initialize_llm(self):
        """Initialize Azure OpenAI LLM."""
        self.llm = AzureChatOpenAI(
            azure_deployment=self.deployment_name,
            azure_endpoint=self.openai_endpoint,
            api_key=self.openai_api_key,
            api_version=self.openai_api_version,
            temperature=0.3,
        )
        print("✓ LLM initialized")

    def create_qa_chain(self, top_k=3):
        """Create the QA chain with retriever and LLM."""
        retriever = self.vector_store.as_retriever(search_kwargs={})

        # Create QA chain directly using RetrievalQA
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
        )
        print("✓ QA chain created")

    def query(self, question):
        """Query the QA system with a question."""
        result = self.qa_chain({"query": question})
        return result

    def format_response(self, result):
        """Format the QA response for display."""
        answer = result["result"]
        sources = result.get("source_documents", [])

        formatted_response = f"Answer: {answer}\n\n"

        if sources:
            formatted_response += "Sources:\n"
            for i, doc in enumerate(sources, 1):
                source = doc.metadata.get("source", "Unknown")
                formatted_response += f"{i}. {source}\n"

        return formatted_response

    def setup(self):
        """Complete setup of the QA system."""
        print("Setting up Document QA System...")
        self.initialize_embeddings()
        documents = self.load_documents()
        chunks = self.split_documents(documents)
        self.initialize_vector_store(chunks)
        self.initialize_llm()
        self.create_qa_chain()
        print("✓ System ready for queries!")


def main():
    # Initialize system
    qa_system = DocumentQASystem()
    qa_system.setup()

    # Interactive query loop
    print("\nEnter your questions (type 'exit' to quit):")
    while True:
        question = input("\nQuestion: ")
        if question.lower() == "exit":
            break

        result = qa_system.query(question)
        formatted = qa_system.format_response(result)
        print(formatted)


if __name__ == "__main__":
    main()
