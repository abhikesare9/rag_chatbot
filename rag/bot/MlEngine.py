from bot.embeddings import GeminiEmbeddingFunction
import google.generativeai as genai
class MLEngine:
    def __init__(self,logger,config,db_client):
        self.logger = logger
        self.config = config
        self.db_client = db_client


    def get_relevant_passage(query: str, db_client, n_results: int):
        results = db_client.query(query_texts=[query], n_results=n_results)
        return [doc[0] for doc in results['documents']]
    
    def make_rag_prompt(query: str, relevant_passage: str):
        escaped_passage = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
        prompt = f"""You are a helpful and informative bot that answers questions using text from the reference passage included below.
        Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
        However, you are talking to a non-technical audience, so be sure to break down complicated concepts and
        strike a friendly and conversational tone.
        QUESTION: '{query}'
        PASSAGE: '{escaped_passage}'

        ANSWER:
        """
        return prompt
    
    def generate_answer(prompt: str):
        gemini_api_key = "AIzaSyAt2LBcxwRFSvdwwqCHv0pmsyN0sgCAEm4"
        if not gemini_api_key:
            raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        result = model.generate_content(prompt)
        return result.text
    


    