import os
import time
from tqdm import tqdm
import configparser

from langchain.embeddings.openai import OpenAIEmbeddings

import chromadb
from langchain.vectorstores import Chroma

# ====================================================================
# 環境変数の取得
# ==================================================================== 
# OpenAI関連
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_MODEL = os.environ.get("AZURE_OPENAI_MODEL")
AZURE_OPENAI_RESOURCE = os.environ.get("AZURE_OPENAI_RESOURCE")

# ====================================================================
# クラス定義
# ==================================================================== 
class vector_db:
    
    def __init__(self, chunkSize, persist_dir):
               
        self.api_type = 'azure'
        self.api_version = '2023-05-15'
        self.api_key = AZURE_OPENAI_KEY
        self.api_base = AZURE_OPENAI_RESOURCE
        self.embeding_deployment = 'text-embedding-ada-002'
        self.embedding_model = 'text-embedding-ada-002'
         
        os.environ["OPENAI_API_TYPE"] = self.api_type
        os.environ["OPENAI_API_VERSION"] = self.api_version
        os.environ["OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_API_BASE"] = f'https://{self.api_base}.openai.azure.com/'
        
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.chunkSize = chunkSize
        
    def mk_db(self, pages, start=0, end=0, units=10, wait=10):
        # ベクトル化用モデルを定義
        embeddings = OpenAIEmbeddings(
            deployment=self.embeding_deployment,
            model=self.embedding_model,
            chunk_size = self.chunkSize,
        )
        
        # create instance
        chroma_index = Chroma(
                collection_name="langchain_store",
                embedding_function=embeddings,
                client=self.client,
            )
        
        if end == 0:
            end = len(pages)
        for i in tqdm(range(start, end, units)):
            time.sleep(wait)
            if i+units > end:
                ed = end
            else:
                ed = i+units

            chroma_index.add_documents(pages[i:ed])
            
        return chroma_index