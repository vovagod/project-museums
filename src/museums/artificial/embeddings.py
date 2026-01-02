import os
import chromadb
import logging
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.utils.embedding_functions.chroma_langchain_embedding_function import create_langchain_embedding
from museums.utils.timeit import timeit
from museums.config import settings_chroma
from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction, Documents
from museums.config import BASE_DIR

logger = logging.getLogger(__name__)


class LangChainEmbeddingAdapter(EmbeddingFunction[Documents]):
    def __init__(self, ef: Embeddings):
        self.ef = ef

    def __call__(self, input: Documents) -> Embeddings:
        # LC EFs also have embed_query but Chroma doesn't support that so we just use embed_documents
        # TODO: better type checking
        return self.ef.embed_documents(input)


@timeit
def main():
    cpu_count = os.cpu_count()
    print(f"Number of CPUs: {cpu_count}")
    inputs = ["что есть равновеликой частью истории отечественного искусства"]
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    # Start a multi-process pool with multiple GPUs
    #pool = model.start_multi_process_pool(target_devices=["cpu", "cpu", "cpu", "cpu"])
    # Encode with multiple GPUs
    #embeddings = model.encode(inputs, pool=pool)
    embeddings = model.encode(
        inputs,
        device=["cpu", "cpu", "cpu", "cpu"],
        #pool=pool,
        #multi_process=True,
        #show_progress=False,
        chunk_size=100
    )
    # Don't forget to stop the pool after usage
    #model.stop_multi_process_pool(pool)
    print(f"EMBEDDINGS: {embeddings}")

@timeit
def main_langchain():
    langchain_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        multi_process=False,
        show_progress=False,
    )
    print(f"LANGCHAIN_EMBEDDINGS: {langchain_embeddings}")

@timeit
def find_sentence():
    #chroma_client = chromadb.Client()
    chroma_client = chromadb.PersistentClient(path=settings_chroma.CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(
        name="museums_data",
        embedding_function=LangChainEmbeddingAdapter(
            HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                model_kwargs={"device": "cpu"}, # "cuda" if torch.cuda.is_available() else "cpu"},
            )
        )
    )
    print(f"COLLECTION: {collection}")
    result_query = collection.query(
        query_texts=["что есть равновеликой частью истории отечественного искусства"], # Chroma will embed this for you
        n_results=3 # how many results to return
    )
    #result_similarity = collection.similarity_search(
        #"человек в социуме"
    #)
    result_search = collection.get(
        where_document={"$contains": "художники из провинции"}
        )
    
    #langchain_embeddings = HuggingFaceEmbeddings(
        #model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        #model_kwargs={"device": "cpu"}, # "cuda" if torch.cuda.is_available() else "cpu"},
        #encode_kwargs={"normalize_embeddings": True},
        #)
    #vector_store = create_langchain_embedding(langchain_embeddings)
    #result_vector = vector_store.similarity_search(
        #"How many distribution centers does Nike have in the US?"
        #)

    print(f"RESULTS_QUERY: {result_query}")
    #print(f"RESULTS_SIMILARITY: {result_similarity}")
    print(f"RESULTS_SEARCH: {result_search}")
    #print(f"RESULTS_VECTOR_STORE: {result_vector}")

def delete_collection():
    chroma_client = chromadb.PersistentClient(path=settings_chroma.CHROMA_PATH)
    chroma_client.delete_collection(name="museums_data")

def create_collection():
    chroma_client = chromadb.PersistentClient(path=settings_chroma.CHROMA_PATH)
    langchain_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        multi_process=False,
        show_progress=False,
    )
    with open(BASE_DIR + "/data/train_result.txt") as file:
        state_of_the_union = file.read()
    # не закончена!!!


if __name__ == "__main__":
    main()
    #main_langchain()
    #find_sentence()
    #delete_collection()