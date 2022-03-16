from typing import Tuple
from prejudice.errors import ConstraintError, ConstraintsErrors
from prejudice.types import Predicate


class Or(Tuple[Predicate]):

    def __call__(self, *args, **namespace):
        errors = []
        for validator in self:
            try:
                validator(*args, **namespace)
            except ConstraintError as exc:
                errors.append(exc)
            except ConstraintsErrors as exc:
                errors.extend(exc.errors)
            else:
                # The validator was successful, stop.
                return
        if errors:
            raise ConstraintsErrors(*errors)
