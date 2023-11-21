# -*- coding: utf-8 -*-
"""Copia de Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o_P1204rcxOqpJvcnVFZ5UM6wCCrSZ40

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
# Visualize the results
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')

print('#SPARQL')
query = prepareQuery(
    """
    SELECT distinct ?subClass
    WHERE {
        ?subClass rdfs:subClassOf* ns:LivingThing
    }
    """,
    initNs={"rdfs": rdfs, 'ns':ns},
)


for row in g.query(query):
    print(row.subClass)

print('#RDFLIB')
def get_subclasses(g,class_name):
  subclasses = set()
  for s,p,o in g.triples((None,RDF.type,RDFS.Class)):
    if (s,RDFS.subClassOf,class_name) in g:
      subclasses.add(s)
      subclasses.update(get_subclasses(g,s))
  return subclasses
subclasses = get_subclasses(g,ns.LivingThing)
for subclass in subclasses:
  print(subclass)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
ns = Namespace("http://somewhere#")
rdfs = Namespace('http://www.w3.org/2000/01/rdf-schema#')
print('#SPARQL')
q1 = prepareQuery(
    """
    SELECT distinct ?individual
    WHERE {
        {
        ?individual a ns:Person.
        }
        UNION
        {
        ?x rdfs:subClassOf* ns:Person.
        ?individual rdf:type ?x
        }
    }
    """,
    initNs={"rdfs": rdfs,"rdf": rdf, "ns": ns}
)
for r in g.query(q1):
  print(r.individual)

print('#RDFLIB')
individuals = set()
for s,p,o in g.triples((None, RDF.type, ns.Person)):
  individuals.add(s)
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for ss,pp,oo in g.triples((None, RDF.type, s)):
    individuals.add(ss)
for individual in individuals:
  print(individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
print('#SPARQL')
query = prepareQuery(
    """
    SELECT distinct ?individual ?properties
    WHERE {
       {
          ?individual a ns:Person.
        }
        UNION
        {
          ?individual a ns:Animal.
        }
        ?individual ?properties ?x
    }
    """,
    initNs={"rdfs": rdfs, "rdf": rdf, "ns": ns}
)
# Visualize the results
for row in g.query(query):
    print(row.individual,row.properties)

print('#RDFLIB')
pairs = set()
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for ss, pp, oo in g.triples((s, None, None)) :
    pairs.add((ss,pp))
for s, p, o in g.triples((None, RDF.type, ns.Animal)):
  for ss, pp, oo in g.triples((s, None, None)) :
    pairs.add((ss,pp))
for pair in pairs:
  print(pair[0],pair[1])

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
print('#SPARQL')
from rdflib import FOAF
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")
query = prepareQuery(
    """
    SELECT ?name
    WHERE {
        ?individual foaf:knows ns:RockySmith.
        ?individual <http://www.w3.org/2001/vcard-rdf/3.0/Given> ?name
    }
    """,
    initNs={'ns':ns, 'vcard': vcard,'foaf':FOAF}
)
# Visualize the results
for row in g.query(query):
    print(row.name)
print('#RDFLIB')

for s, p, o in g.triples((None, FOAF.knows, ns.RockySmith)):
  print(s)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

print('#SPARQL')
query = prepareQuery(
    '''
    SELECT ?entity
    WHERE {
        ?entity foaf:knows ?known .
    }
    GROUP BY ?entity
    HAVING (COUNT(?known) >= 2)
    ''',
    initNs={'foaf':FOAF}
)
# Visualize the results
for row in g.query(query):
    print(row.entity)

print("#RDFLIB")
count = {}
for s, p, o in g.triples((None, FOAF.knows, None)):
  count[s] = count.get(s,0)+1
entities = [entity for entity, freq in count.items() if freq >= 2]
for entity in entities:
  print(entity)
