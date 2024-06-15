import owlready2
import argparse
import os

def load_ontology(path):
    """ Load the ontology from the given path."""
    return owlready2.get_ontology(path).load()

def get_args():
    # Add -i input, -o output, -a algorithm
    parser = argparse.ArgumentParser(description='Process some integers.')
    
    # input1 and input2
    parser.add_argument('-i', '--input', type=str, help='Input ontology file path', default=os.path.join('res', 'ekaw.owl'))
    parser.add_argument('-i2', '--input2', type=str, help='Input ontology file path', default='res/confOf.owl')

    parser.add_argument('-o', '--output', type=str, help='Output ontology file path', default='output/alignment.ttl')
    parser.add_argument('-r', '--reference', type=str, help='Reference mappings file path', default='res/reference_mappings.ttl')
    parser.add_argument('-a', '--algorithm', type=str, help='Algorithm to use', default='baseline')
    return parser.parse_args()