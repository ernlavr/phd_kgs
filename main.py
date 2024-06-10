import src.utils.utils as utils
import src.processing.baseline as bs
from src.utils.ontoloty_loader import OntologyLoader

def main():
    args = utils.get_args()

    kg_1 = OntologyLoader(args.input)
    kg_2 = OntologyLoader(args.input2)

    match args.algorithm:
        case "baseline":
            bs.get_class_alignment(kg_1, kg_2, args.output)
        case _:
            print("No algorithm specified")
    

if __name__ == '__main__':
    main()



