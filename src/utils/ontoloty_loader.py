'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *
from rdflib import Graph
import os

class OntologyLoader():
    def __init__(self, path):
        self.path = path
        self.onto = get_ontology(path).load()

    def getName(self):
        path = self.getPath()
        return os.path.basename(path).split('.')[0]

    def getPath(self):
        return self.path

    def getClasses(self):        
        return self.onto.classes()
        
    def getDataProperties(self):        
        return self.onto.data_properties()
        
    def getObjectProperties(self):        
        return self.onto.object_properties()
        
    def getIndividuals(self):    
        return self.onto.individuals()


    def getRDFSLabelsForEntity(self, entity):
        #if hasattr(entity, "label"):
        return entity.label


    def getRDFSLabelsForEntity(self, entity):
        #if hasattr(entity, "label"):
        return entity.label    


    def loadOntology(self, urionto):
        
        #Method from owlready
        self.onto = get_ontology(urionto).load()
        
        print("Classes in Ontology: " + str(len(list(self.getClasses()))))
        for cls in self.getClasses():
            #Name of entity in URI. But in some cases it may be a 
            #code like in mouse and human anatomy ontologies                
            print(cls.iri)
            print("\t"+cls.name)  
            #Labels from RDFS label
            print("\t"+str(self.getRDFSLabelsForEntity(cls)))