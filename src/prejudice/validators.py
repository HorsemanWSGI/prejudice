from typing import Tuple
from prejudice.errors import ConstraintError, ConstraintsErrors
from prejudice.types import Predicate


class Or(Tuple[Predicate]):

    def __call__(self, *args, **namespace):
        errors = []
        for validator in self:
            try:
                validator(*args, **namespace)
                return
            except ConstraintError as exc:
                errors.append(exc)
            except ConstraintsErrors as exc:
                errors.extend(exc.errors)
        if errors:
            raise ConstraintsErrors(*errors)
