from bson import ObjectId

def serialize_mongo_document(doc):
    """
    Recursively converts MongoDB ObjectIds to strings for JSON serialization.
    """
    if isinstance(doc, dict):
        return {key: serialize_mongo_document(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_mongo_document(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    return doc
