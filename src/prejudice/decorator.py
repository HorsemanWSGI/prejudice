from functools import wraps
from typing import Optional
from prejudice.errors import ConstraintError, ConstraintsErrors
from prejudice.types import Predicates, PredicateErrorHandler


def with_predicates(
        predicates: Predicates,
        handler: Optional[PredicateErrorHandler] = None):
    def predication_wrapper(func):
        @wraps(func)
        def assert_predicates(*args, **kwargs):
            for predicate in predicates:
                try:
                    predicate(*args, **kwargs)
                except (ConstraintError, ConstraintsErrors) as exc:
                    if handler is not None:
                        return handler(exc)
                    raise
            return func(*args, **kwargs)
        return assert_predicates
    return predication_wrapper
