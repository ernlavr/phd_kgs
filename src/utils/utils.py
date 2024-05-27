import owlready2

def load_ontology(path):
    """ Load the ontology from the given path."""
    return owlready2.get_ontology(path).load()