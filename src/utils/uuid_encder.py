import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def uuid_dumps(*args, **kwargs):
    return json.dumps(cls=UUIDEncoder, *args, **kwargs)
