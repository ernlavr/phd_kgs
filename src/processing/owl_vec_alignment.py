from owl2vec_star import owl2vec_star as o2v
from gensim.models import KeyedVectors
import os


def _try_get_cached_model(path):
    try:
        return KeyedVectors.load(path, mmap='r')
    except FileNotFoundError:
        return None
    
def get_embeddings(kg, recompute=False):
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
    pass