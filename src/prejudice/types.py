import typing as t
from prejudice import errors


Error = t.Union[
    errors.ConstraintError,
    errors.ConstraintsErrors
]
Predicate = t.Callable[..., t.Any]
Predicates = t.Iterable[Predicate]
PredicateErrorHandler = t.Callable[[Error], t.Any]
