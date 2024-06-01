import Levenshtein as lev 
from src.utils.isub import isub
from src.utils.ontoloty_loader import OntologyLoader
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, FOAF, XSD
import sklearn
from src.utils.evaluation import compareWithReference
from tqdm import tqdm
import os

def get_class_alignment(onto_1: OntologyLoader, onto_2: OntologyLoader, output_name: str, debugging=False):
    g = Graph()
    ns = Namespace("https://dbpedia.org/ontology/")

    # Pair-wise compare classes
    for i in tqdm(onto_1.getClasses(), "Classes.."):
        for j in onto_2.getClasses():
            i_name = i.get_name(i)
            j_name = j.get_name(j)

            if isub(i_name, j_name) > 0.9:
                i_ent = URIRef(i.get_iri(i))
                j_ent = URIRef(j.get_iri(j))
                g.add((i_ent, OWL.equivalentClass, j_ent))
        
        # Cut early if we wanna debug
        if debugging and i > 10:
            break

    # Pair-wise compare properties
    for i in tqdm(onto_1.getObjectProperties(), "Properties.."):
        for j in onto_2.getObjectProperties():
            i_name = i.get_name()
            j_name = j.get_name()

            if isub(i_name, j_name) > 0.9:
                i_ent = URIRef(i.get_iri())
                j_ent = URIRef(j.get_iri())
                g.add((i_ent, OWL.equivalentProperty, j_ent))
        
        # Cut early if we wanna debug
        if debugging and i > 10:
            break

    # check if output_name folder exists
    os.makedirs(os.path.dirname(output_name), exist_ok=True)

    g.serialize(destination=output_name, format='ttl')
    return g