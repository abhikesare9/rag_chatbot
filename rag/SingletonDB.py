import chromadb
from threading import Lock
from RagConfigParser import MLConfigParser
from RagLogger import SingletonLogger
from bot.embeddings import GeminiEmbeddingFunction
from typing import List

class ChromaDBSingleton():
    _chroma_instance = None
    _chroma_lock = Lock()

    def __new__(cls):
        if not cls._chroma_instance:
            with cls._chroma_lock:
                if not cls._chroma_instance:
                    cls._chroma_instance = super(ChromaDBSingleton, cls).__new__(cls)
                    cls._chroma_instance._initialize_chromadb()
        return cls._chroma_instance
    
    
    def _initialize_chromadb(self):
        """Initialize ChromaDB connection."""
        self.config = MLConfigParser()
        self.logger = SingletonLogger().get_logger()
        chroma_host = self.config.get("DB_Config","DB_HOST")
        chroma_port = self.config.get("DB_Config","DB_PORT")
        self.logger.info(f'db configuration is {chroma_host}, {chroma_port}')

        self.client = chromadb.HttpClient(host=chroma_host, port=int(chroma_port))
        self.logger.info("successfully connected to chromadb")

    def get_client(self):
        try:
            return self.client
        except Exception as e:
            self.logger.error("Failed to get client from chromdb")
    
    def create_collection(self,collection_name):
        try:
            client_object = self.get_client()
            create_collection =  client_object.create_collection(name=collection_name)
            return create_collection
        except Exception as e:
            raise f"Failed to create collection: {e}"
        
    def delete_chromadb(self,collection_name):
        chroma_client = self.get_client()
        output = chroma_client.delete_collection(name=collection_name)
        print(output)

        
    def create_chroma_db(self,documents, name: str):
        chroma_client = self.get_client()
        db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())
        for i, d in enumerate(documents):
            db.add(documents=[d], ids=[str(i)])
        return db, name
        
    def load_chroma_collection(self, name: str):
        chroma_client = self.get_client()
        return chroma_client.get_collection(name=name, embedding_function=GeminiEmbeddingFunction())
    



    



