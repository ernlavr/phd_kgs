from rdflib import OWL, Graph, URIRef
from owl2vec_star import owl2vec_star as o2v
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
import gensim



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

def get_properties_classes(model: gensim.models.word2vec.Word2Vec):
    """
    Parameters:
        model: The Word2Vec model from which to extract properties and classes.

    Returns:
        properties (dict): Keys are property URIs and values are their corresponding vectors.
        classes (dict): Keys are class URIs and values are their corresponding vectors.
    """

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
    # Retrieve embeddings
    model_kg_1 = get_embeddings(kg_1, "res/default_kg1.cfg")
    model_kg_2 = get_embeddings(kg_2, "res/default_kg2.cfg")

    # Retrieve properties and classes
    props_kg1, classes_kg1 = get_properties_classes(model_kg_1)
    props_kg2, classes_kg2 = get_properties_classes(model_kg_2)

    # Get equals according to cosine similarity
    equal_classes = _compute_cosines(classes_kg1, classes_kg2, 0.8)
    equal_props = _compute_cosines(props_kg1, props_kg2, 0.8)

    # Serialize
    serialize_into_graph(equal_classes, equal_props, output)


def serialize_into_graph(equal_classes: list, equal_properties: list, output_name: str):
    """
    This function takes in two lists of equivalent classes and properties, and an output name. 
    It creates a graph using these classes and properties, and then serializes this graph into a 
    Turtle (ttl) format file with the given output name.

    Parameters:
    equal_classes (list): A list of tuples where each tuple contains two equivalent classes.
    equal_properties (list): A list of tuples where each tuple contains two equivalent properties.
    output_name (str): The name of the output file where the serialized graph will be saved.

    Returns:
    g (rdflib.Graph): The created and serialized graph.
    """
    g = Graph()
    # Pair-wise compare classes
    for i in tqdm(equal_classes, "Classes.."):
        rdf_term1 = URIRef(i[0])
        rdf_term2 = URIRef(i[1])
        g.add((rdf_term1, OWL.equivalentClass, rdf_term2))
        
    for i in tqdm(equal_properties, "Properties.."):
        rdf_term1 = URIRef(i[0])
        rdf_term2 = URIRef(i[1])
        g.add((rdf_term1, OWL.equivalentProperty, rdf_term2))
    
    # check if output_name folder exists
    os.makedirs(os.path.dirname(output_name), exist_ok=True)
    g.serialize(destination=output_name, format='ttl')
    return g

