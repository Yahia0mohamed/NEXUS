import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# Local DB storage
PERSIST_DIRECTORY = os.getenv("VECTOR_DB_PATH", "vector_store")

class VectorDB:
    def __init__(self):
        # Local embedding model (small & fast)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = None

    def init_db(self):
        """Initialize or load the vector store."""
        self.db = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )

    def add_document(self, content: str, metadata: dict = None):
        """Add a single document to the vector store."""
        if not self.db:
            self.init_db()
        self.db.add_texts([content], metadatas=[metadata or {}])
        self.db.persist()

    def retrieve_similar(self, query: str, top_k: int = 3):
        """Retrieve top K most relevant documents for the query."""
        if not self.db:
            self.init_db()
        results = self.db.similarity_search(query, k=top_k)
        return "\n\n".join([doc.page_content for doc in results])

    def clear(self):
        """Clear the vector DB (use with caution)."""
        if not self.db:
            self.init_db()
        self.db.delete_collection()
