from RagConfigParser import MLConfigParser
from RagLogger import SingletonLogger
from SingletonDB import ChromaDBSingleton
from utils import Utils
from fastapi import FastAPI, File, UploadFile
from bot.MlEngine import MLEngine
import uvicorn
import os
import shutil
import uuid
logger = SingletonLogger().get_logger()
config = MLConfigParser()
db_client = ChromaDBSingleton()
mlengine = MLEngine(logger=logger,config=config,db_client=db_client)
app = FastAPI()


@app.get("/")
def welcome():
    return "welcome to rag_chatbot"


@app.post("/bot")
def rag_bot(input_query: str, file: UploadFile = File(...)):
    try:
        file_path = os.path.join("pdfs/", file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        read_pdf = Utils.load_pdf(file_path)
        split_text = Utils.split_text(read_pdf)
        logger.info("Text extracted from pdf and converted into chunks")
        
        try:
            delete_file = db_client.delete_chromadb(file.filename)
            db, create_db = db_client.create_chroma_db(split_text,file.filename)
            logger.info(create_db)
            load_chroma_collection =  db_client.load_chroma_collection(name=file.filename)
            logger.info(load_chroma_collection)
            try:
                get_relevent_passage = str(mlengine.get_relevant_passage(input_query,db,n_results=1))
                try:
                    make_rag_prompt= mlengine.make_rag_prompt(input_query,get_relevent_passage)
                    try:
                        generate_answer = mlengine.generate_answer(make_rag_prompt)
                        return generate_answer
                    except Exception as e:
                        logger.error(f"Failed to generate answer {e}")
                        raise e
                except Exception as e:
                    logger.error(f'Failed to make rag prompt {e}')
                    raise e
            except Exception as e:
                logger.error("Failed to get relevent passage, Please change the query")
                raise e
        except Exception as e:
            logger.error(f"Failed to perform db operations {e}")
    except Exception as e:
        logger.info("Invalid query")
        raise e

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)