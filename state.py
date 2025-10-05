import copy
import json
from datetime import date, datetime
from decimal import Decimal

class _SafeEncoder(json.JSONEncoder):
    def default(self, obj):
        # Common helpful conversions:
        if isinstance(obj, (set, tuple)):
            return list(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            try:
                return float(obj)
            except Exception:
                return str(obj)
        # Fallback: keep it visible as a string
        return repr(obj)

def _stringify_keys(obj):
    if isinstance(obj, dict):
        return {str(k): _stringify_keys(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_stringify_keys(v) for v in obj]
    return obj



class State(dict):
    def __init__(self, *args, _no_deepcopy_keys=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
        self._no_deepcopy_keys = set(_no_deepcopy_keys or [])

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls(_no_deepcopy_keys=self._no_deepcopy_keys)
        memo[id(self)] = result

        for k, v in self.items():
            if k in self._no_deepcopy_keys:
                # Preserve this key by reference (no deepcopy)
                result[k] = v
            else:
                result[k] = copy.deepcopy(v, memo)

        result.__dict__ = result
        return result

    def duplicate(self):
        return copy.deepcopy(self)

    def __str__(self):
        safe_view = _stringify_keys(self)
        return json.dumps(safe_view, indent=4, sort_keys=True, cls=_SafeEncoder)

    __repr__ = __str__