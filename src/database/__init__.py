from elasticsearch_dsl.connections import connections
from dotenv import load_dotenv
import os


load_dotenv()


def elasticsearch_connection():
    return connections.create_connection(hosts=[os.getenv("HOST")])
