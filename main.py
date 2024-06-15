import sys
sys.path.append('OWL2Vec-Star')
sys.path.append('OWL2Vec-Star/owl2vec_star')
sys.path.append('OWL2Vec-Star/owl2vec_star/lib/')
sys.path.append('OWL2Vec-Star/owl2vec_star/rdf2vec/')

import src.utils.utils as utils
import src.processing.baseline as bs
import src.processing.owl_vec_alignment as ova
from src.utils.ontoloty_loader import OntologyLoader

def main():
    args = utils.get_args()

    kg_1 = OntologyLoader(args.input)
    kg_2 = OntologyLoader(args.input2)

    if args.algorithm == "baseline":
        bs.get_class_alignment(kg_1, kg_2, args.output)
    elif args.algorithm == 'owl2vec':
        ova.get_class_alignment(kg_1, kg_2, args.output)
    else:
        print("No algorithm specified")
    

if __name__ == '__main__':
    main()