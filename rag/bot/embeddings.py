import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        gemini_api_key = "AIzaSyAt2LBcxwRFSvdwwqCHv0pmsyN0sgCAEm4"
        genai.configure(api_key=gemini_api_key)
        model = "models/embedding-001"
        title = "Custom query"
        return genai.embed_content(model=model, content=input, task_type="retrieval_document", title=title)["embedding"]
