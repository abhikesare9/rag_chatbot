import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
from RagConfigParser import MLConfigParser
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        config = MLConfigParser()
        api_key = config.get("MLEngine","GOOGLE_API_KEY")
        gemini_api_key = api_key
        genai.configure(api_key=gemini_api_key)
        model = "models/embedding-001"
        title = "Custom query"
        return genai.embed_content(model=model, content=input, task_type="retrieval_document", title=title)["embedding"]
