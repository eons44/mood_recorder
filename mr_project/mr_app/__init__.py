import os

from neo4j import GraphDatabase

uri = os.environ['NEO4J_URI']
user = os.environ['NEO4J_USER']
password = os.environ['NEO4J_PASSWORD']

DRIVER = GraphDatabase.driver(uri, auth=(user, password))