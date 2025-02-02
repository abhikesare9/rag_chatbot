from RagConfigParser import MLConfigParser
from RagLogger import SingletonLogger
from SingletonDB import ChromaDBSingleton
import utils
from fastapi import FastAPI
from bot.MlEngine import MLEngine


logger = SingletonLogger()
config = MLConfigParser()
db_client = ChromaDBSingleton(singletonlogger=logger,configsigleton=config)
mlengine = MLEngine(logger=logger,config=config,db_client=db_client)
app = FastAPI()


@app.route("/")
def welcome():
    return "welcome to rag_chatbot"


# @app.route("/bot")
# def rag_bot(input_query: str):
#     try:
#         collection = db_client.load_chroma_collection(db_name)
#         try:
#             relevant_text = mlengine.get_relevant_passage(input_query, db, n_results=1)
#             final_prompt = mlengine.make_rag_prompt(input_query, "".join(relevant_text))
#             answer = mlengine.generate_answer(final_prompt)
#             return answer
#         except Exception as e:
#             logger.info(f"No relevent text found in document {e}")
#     except Exception as e:
#         logger.info("Invalid query")
#         raise e

if __name__ == "__main__":
    app.run()