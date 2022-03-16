import pytest
from prejudice.errors import (
    ConstraintError, HTTPConstraintError, ConstraintsErrors,
)


def test_httperror_malformed():
    with pytest.raises(TypeError) as exc:
        HTTPConstraintError()

    assert str(exc.value) == (
        "__init__() takes at least 1 positional argument (0 given)"
    )

    with pytest.raises(TypeError) as exc:
        HTTPConstraintError(status=303)

    assert str(exc.value) == (
        "__init__() takes at least 1 positional argument (0 given)"
    )

    with pytest.raises(ValueError) as exc:
        HTTPConstraintError(message='test', status='abc')

    assert str(exc.value) == "'abc' is not a valid HTTPStatus"


def test_httperror():
    error = HTTPConstraintError(message='test')
    assert error.status == 400

    error = HTTPConstraintError(message='test', status=404)
    assert error == HTTPConstraintError(message='test', status=404)

    with pytest.raises(AttributeError) as exc:
        error.message = 'I am immutable'

    with pytest.raises(AttributeError) as exc:
        error.status = 200

    error = HTTPConstraintError('test', 400)
    assert error == HTTPConstraintError(message='test', status=400)


def test_httperrors():
    error1 = ConstraintError('test 1')
    error2 = HTTPConstraintError('test 2', 400)

    errors = ConstraintsErrors(error1, error2)
    assert len(errors) == 2
    assert errors == ConstraintsErrors(error1, error2)
    assert errors == [error1, error2]
    assert not errors == (error1, error2)

    assert errors.json() == (
        '''[{"message": "test 1"}, {"message": "test 2"}]'''
    )
