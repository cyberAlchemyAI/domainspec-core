from uuid import uuid4
from typing import Any

from .contracts import StructuredError, GateFailure

class SubstrateError(Exception):
    def __init__(self, status_code: int, error: StructuredError):
        super().__init__(error.message)
        self.status_code = status_code
        self.error = error

    @property
    def code(self):
        return self.error.code
