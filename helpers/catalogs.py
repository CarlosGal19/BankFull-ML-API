def serialize_catalog(query_result):
    return [{"id": item.id, "name": item.name, "abreviation": getattr(item, "abreviation", None)}
            for item in query_result]
