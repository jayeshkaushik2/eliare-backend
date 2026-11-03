from app.schemas.database import db_container
from bson import ObjectId


sync_db = db_container.sync_db
MongoTables = {
    "error_logs",
    "users"
}
# when this file is imported, it will automatically connect to the MongoDB database and provide access to the specified tables.

def all_mongo_documents(table_name: str):
    if table_name not in MongoTables:
        raise ValueError("Invalid table name")

    table = sync_db.get_collection(table_name)
    # table.all

def get_mongo_document(table_name: str, _id: str | None = None, load: bool = False, **kwargs):
    """
    Get a document from the specified MongoDB table based on the provided query.

    Args:
        table_name (str): The name of the MongoDB table.
        query (dict): The query to filter documents.
    """
    if table_name not in MongoTables:
        raise ValueError(f"Invalid table name: {table_name}")

    table = sync_db.get_collection(table_name)
    if _id:
        return table.find_one({"_id": ObjectId(_id)})

    res = table.find(kwargs)
    results = []
    if load:
        for document in res:
            results.append(document)
        return results
    return res