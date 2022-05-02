from tkinter import *
from owlready2 import *


class Ontology:
    prefix = ""
    obo = ""
    go = ""

    # parameterized constructor
    def __init__(self, ontology_path, ontology_namespace):
        self.prefix = ontology_namespace
        self.obo = get_namespace(ontology_namespace)
        self.go = get_ontology(ontology_path).load()

    def ancestors(self, FMAID):
        ancestors = list(default_world.sparql("""
                           prefix : <http://purl.org/sig/ont/fma/>
                           prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                           select ?superclass where {
                             :%s rdfs:subClassOf* ?superclass
                           }
                    """ % ('fma' + FMAID)))
        return ancestors

    def properties(self, FMAID):
        props = list(default_world.sparql("""
                   prefix : <http://purl.org/sig/ont/fma/>
                   select ?property ?value where {
                     ?class :FMAID %s ;
                            rdfs:subClassOf [ owl:hasValue ?value ;
                                              owl:onProperty [ rdfs:label ?property ] ] .
                   }
            """ % FMAID))
        return props

    def subclasses(self, FMAID):
        return list(self.obo[('fma' + FMAID)].subclasses())
