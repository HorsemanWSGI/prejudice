import json
from http import HTTPStatus
from typing import List, Iterable, TypeVar


HTTPCode = TypeVar('HTTPCode', HTTPStatus, int)


cdef class ConstraintError(Exception):

    cdef readonly str message
    cdef object __weakref__ # enable weak referencing support

    def __init__(self, message: str):
        self.message = message

    def __eq__(self, error):
        if isinstance(error, self.__class__):
            return error.message == self.message
        return False

    def to_dict(self):
        return {
            "message": self.message
        }


cdef class HTTPConstraintError(ConstraintError):

    cdef readonly unsigned int status

    def __init__(self, message: str, status: HTTPCode = 400):
        self.message = message
        self.status = HTTPStatus(status)

    def __eq__(self, error):
        if isinstance(error, self.__class__):
            return (
                error.message == self.message and
                self.status == error.status
            )
        return False


cdef class ConstraintsErrors(Exception):

    cdef public list errors

    def __init__(self, *errors: ConstraintError):
        self.errors: List[ConstraintError] = list(errors)

    def __iter__(self):
        return iter(self.errors)

    def __len__(self):
        return len(self.errors)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.errors == other.errors
        elif isinstance(other, Iterable):
            return self.errors == other
        return False

    cpdef str json(self):
        return json.dumps([e.to_dict() for e in self.errors])
