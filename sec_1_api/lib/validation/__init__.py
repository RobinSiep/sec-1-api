import bleach
from marshmallow.fields import Field


class CleanString(Field):
    def _serialize(self, value, attr, obj):
        if not value:
            return ''
        return bleach.clean(value, tags=[], strip=True)
