import pytest
from prejudice.errors import ConstraintError, ConstraintsErrors
from prejudice.decorator import with_predicates


class Document:

    def __init__(self, id):
        self.id = id


def assert_not_empty(item):
    if item is None:
        raise ConstraintError('No null object allowed.')


def validate_document(doc):
    errors = []
    if not doc:
        errors.append(ConstraintError('Document is empty.'))
    if not getattr(doc, 'id', None):
        errors.append(ConstraintError('Document does not have an id.'))
    if errors:
        raise ConstraintsErrors(*errors)


def test_simple_decorator():

    @with_predicates([validate_document])
    def handle_doc(doc):
        return True


    with pytest.raises(ConstraintsErrors) as err:
        handle_doc(None)

    assert err.value.json() == (
        '[{"message": "Document is empty."}, '
        '{"message": "Document does not have an id."}]'
    )

    assert handle_doc(Document('abc')) is True


    @with_predicates([assert_not_empty, validate_document])
    def handle_doc(doc):
        return True

    with pytest.raises(ConstraintError) as err:
        handle_doc(None)

    assert err.value.message == "No null object allowed."
