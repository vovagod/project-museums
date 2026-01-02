import chromadb
#import torch
from chromadb.utils.embedding_functions.chroma_langchain_embedding_function import create_langchain_embedding
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from museums.config import settings_chroma

from museums.config import BASE_DIR


# Load example document
with open(BASE_DIR + "/data/train_result.txt") as file:
    state_of_the_union = file.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=10,
    length_function=len,
    is_separator_regex=False,
)

text_splitter_character = CharacterTextSplitter(
    separator=".", #"\n\n",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)
texts_character = text_splitter_character.split_text(state_of_the_union)
print(f"TEXTS_CHARACTER: {texts_character}")
ids = [str(i) for i in range(1, len(texts_character)+1)]
documents = [item for item in texts_character]


metadatas = [{"document": 1}]
texts = text_splitter.create_documents(
    [state_of_the_union],
    #metadatas = metadatas
    )
print(len(texts))
print(texts)
#print(texts[1])
#ids = [str(i) for i in range(1, len(texts)+1)]
#documents = [item.page_content for item in texts]


langchain_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    #model_kwargs={"device": "cpu"}, # "cuda" if torch.cuda.is_available() else "cpu"},
    #encode_kwargs={"normalize_embeddings": True},
    )
ef = create_langchain_embedding(langchain_embeddings)
client = chromadb.PersistentClient(path=settings_chroma.CHROMA_PATH)
collection = client.get_or_create_collection(name="museums_data", embedding_function=ef)

collection.add(ids=ids,documents=documents)

#sentences = ["This is an example sentence", "Each sentence is converted"]
#model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
#embeddings = model.encode(sentences)
#print(f"EMBEDDINGS: {embeddings}")

'''
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="museums_data")
results = collection.query(
    query_texts=["часть истории отечественного искусства XVIII"], # Chroma will embed this for you
    n_results=2 # how many results to return
)
print(f"RESULTS_FOUND: {results}")
'''