from datetime import datetime
from enum import Enum
import os


from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from log_config import logger


class State(Enum):
    PENDING = 1
    PROCESSED = 2


class TitleModel(Model):
    class Meta:
        table_name = os.environ["DYNAMODB_TABLE"]
        if "ENV" in os.environ:
            host = "http://localhost:8000"
        else:
            region = "eu-central-1"
            host = os.environ["DYNAMODB_HOST"]

    request_id = UnicodeAttribute(hash_key=True, null=False)
    title = UnicodeAttribute(null=True)
    state = UnicodeAttribute(null=False, default=State.PENDING.name)
    url = UnicodeAttribute(null=False)
    s3_url = UnicodeAttribute(null=True)
    createdAt = UTCDateTimeAttribute(null=False, default=datetime.now().astimezone())
    updatedAt = UTCDateTimeAttribute(null=False, default=datetime.now().astimezone())

    def __str__(self):
        return f"request_id: {self.request_id}, title: {self.title}"

    def save(self, conditional_operator=None, **expected_values):
        try:
            self.updatedAt = datetime.now().astimezone()
            logger.debug(f"saving: {self}")
            super(TitleModel, self).save()
        except Exception as e:
            logger.error(f"saving {self.request_id} failed: {e}", exc_info=True)
            raise e

    def __iter__(self):
        for name, attr in self._get_attributes().items():
            yield name, attr.serialize(getattr(self, name))
