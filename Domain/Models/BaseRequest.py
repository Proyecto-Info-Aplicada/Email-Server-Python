import uuid
import datetime

class BaseRequest:
    def __init__(self, path: str):
        self.correlation_id = str(uuid.uuid4())
        self.path = path
        self.timestamp = datetime.datetime.now().isoformat()
