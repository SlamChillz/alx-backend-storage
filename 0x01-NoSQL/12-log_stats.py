#!/usr/bin/env python3
"""
A script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stat() -> None:
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    stats = ""
    client = MongoClient('mongodb://127.0.01:27017')
    nginx_collection = client.logs.nginx
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    stats += "{} logs\nMethods:\n".format(nginx_collection.count_documents({}))
    for m in method:
        method_count = nginx_collection.count_documents({"method": m})
        stats += '{}method {}: {}\n'.format(' '*4, m, method_count)
    stats += "{} status check".format(
        nginx_collection.count_documents({"path": "/status"}))
    print(stats)


if __name__ == '__main__':
    log_stat()
