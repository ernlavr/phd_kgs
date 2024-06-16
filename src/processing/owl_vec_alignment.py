from owl2vec_star import owl2vec_star as o2v
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



def _try_get_cached_model(path):
    try:
        return KeyedVectors.load(path, mmap='r')
    except FileNotFoundError:
        return None
    
def get_embeddings(kg, config, recompute=False):
    os.makedirs("output", exist_ok=True)
    cached = _try_get_cached_model(os.path.join("output", f"{kg.getName()}_ontology.embeddings"))
    if cached is not None and recompute is False:
        return cached

    model = o2v.extract_owl2vec_model(kg.path, config, True, True, True)
    model.save(os.path.join("output", f"{kg.getName()}_ontology.embeddings"))
    return model

def get_properties_classes(model):
    wv = model.wv
    properties = {}
    classes = {}
    for key in wv.index_to_key:
        # Avoid RDF schemas
        if 'rdf-schema' in key or 'owl' in key: 
            continue

        s = key.split('#')
        if len(s) > 1:
            if s[-1][0].isupper(): # first char of the split http://xx#Yyy is uppercase
                classes[key] = wv.get_vector(key)
            else:
                properties[key] = wv.get_vector(key)
    return properties, classes

def _compute_cosines(kg1, kg2, threshold):
    equals = []
    for kg1_k, kg1_v in kg1.items():
        for kg2_k, kg2_v in kg2.items():
            sim = cosine_similarity([kg1_v], [kg2_v])[0][0]
            if sim > threshold:
                equals.append((kg1_k, kg2_k))
    return equals

def get_class_alignment(kg_1, kg_2, output):
    print("Implement owl2vec")
    model_kg_1 = get_embeddings(kg_1, "res/default_kg1.cfg")
    model_kg_2 = get_embeddings(kg_2, "res/default_kg2.cfg")

    props_kg1, classes_kg1 = get_properties_classes(model_kg_1)
    props_kg2, classes_kg2 = get_properties_classes(model_kg_2)


    equal_classes = _compute_cosines(classes_kg1, classes_kg2, 0.8)
    equal_props = _compute_cosines(props_kg1, props_kg2, 0.8)
    
    df_kg1 = pd.DataFrame.from_dict(embedding_dict_kg_1, orient='index')
    df_kg2 = pd.DataFrame.from_dict(embedding_dict_kg_2, orient='index')

    kg1PC = get_pca(df_kg1, 30)
    kg2PC = get_pca(df_kg2, 30)


    pairwise_matrix = cosine_similarity(df_kg1, df_kg2)
    pairwise_matrix_cossim_PC = cosine_similarity(kg1PC, kg2PC)


    for i, kg2_row in enumerate(pairwise_matrix_cossim_PC):
        # get kg2_row all indices that are above 0.9
        indices = np.where(kg2_row > 0.8)
        if len(indices[0]) == 0:
            continue

        max_idx = max(indices[0])
        kg1_class = df_kg1.iloc[i].name
        kg2_class = df_kg2.iloc[max_idx].name
        print(f"{kg1_class} -> {kg2_class} - {kg2_row[max_idx]}")

    pass

def get_pca(df, dim):
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)
    #print (scaled_df[1].mean(), scaled_df[1].std())
    pca = PCA(n_components=dim)
    principalComponents = pca.fit_transform(scaled_df)
    principalDf = pd.DataFrame(data = principalComponents)
    print(pca.explained_variance_ratio_.sum(), "Cumulative Variance Ratio")
    return principalDf

