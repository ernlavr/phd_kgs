from owl2vec_star import owl2vec_star as o2v
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os


def _try_get_cached_model(path):
    try:
        return KeyedVectors.load(path, mmap='r')
    except FileNotFoundError:
        return None
    
def get_embeddings(kg, recompute=False):
    os.makedirs("output", exist_ok=True)
    cached = _try_get_cached_model(os.path.join("output", f"{kg.getName()}_ontology.embeddings"))
    if cached is not None and recompute is False:
        return cached

    model = o2v.extract_owl2vec_model(kg.path, "res/default.cfg", True, True, True)
    model.save(os.path.join("output", f"{kg.getName()}_ontology.embeddings"))
    return model



def get_class_alignment(kg_1, kg_2, output):
    print("Implement owl2vec")
    model_kg_1 = get_embeddings(kg_1)
    model_kg_2 = get_embeddings(kg_2)

    wv1 = model_kg_1.wv

    wv2 = model_kg_2.wv

    embedding_dict_kg_1 = {}
    for key in wv1.index_to_key:
        embedding_dict_kg_1[key] = wv1.get_vector(key)

    embedding_dict_kg_2 = {}
    for key in wv2.index_to_key:
        embedding_dict_kg_2[key] = wv2.get_vector(key)
    
    df_kg1 = pd.DataFrame.from_dict(embedding_dict_kg_1, orient='index')
    df_kg2 = pd.DataFrame.from_dict(embedding_dict_kg_2, orient='index')

    pairwise_matrix = cosine_similarity(df_kg1, df_kg2)


    pass

