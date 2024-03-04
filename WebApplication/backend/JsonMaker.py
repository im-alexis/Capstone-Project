import json
from typing import Any
from bson import ObjectId


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)