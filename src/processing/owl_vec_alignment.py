from owl2vec_star import owl2vec_star as o2v
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import numpy as np
from sklearn.decomposition import PCA


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

    kg1PC = get_pca(df_kg1, 10)
    kg2PC = get_pca(df_kg2, 10)


    pairwise_matrix = cosine_similarity(df_kg1, df_kg2)
    pairwise_matrix_cossim_PC = cosine_similarity(kg1PC, kg2PC)


    for i, kg2_row in enumerate(pairwise_matrix_cossim_PC):
        # get kg2_row all indices that are above 0.9
        indices = np.where(kg2_row > 0.9)
        if len(indices[0]) == 0:
            continue

        max_idx = max(indices[0])
        kg1_class = df_kg1.iloc[i].name
        kg2_class = df_kg2.iloc[max_idx].name
        print(f"{kg1_class} -> {kg2_class} - {kg2_row[max_idx]}")

    pass

def get_pca(df, dim=20):
    pca = PCA(n_components=dim)
    principalComponents = pca.fit_transform(df)
    principalDf = pd.DataFrame(data = principalComponents)
    return principalDf

