from prejudice.errors import ConstraintError, ConstraintsErrors
from prejudice.types import Predicates


cpdef _resolve(tuple validators, tuple args, dict namespace):
    cdef list errors = []
    for validator in validators:
        try:
            validator(*args, **namespace)
        except ConstraintError as exc:
            errors.append(exc)
        except ConstraintsErrors as exc:
            errors.extend(exc.errors)
    if errors:
        return ConstraintsErrors(*errors)


def resolve_constraints(validators: Predicates, *args, **kwargs):
    return _resolve(tuple(validators), args, kwargs)
