from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'

DRIVER = GraphDatabase.driver(uri, auth=('neo4j', 'password'))

USERS = ['Rob', 'Seon', 'Taylor', 'Udam']
EMOTIONS = ['ecstatic', 'happy', 'sad', 'furious']