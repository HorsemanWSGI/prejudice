import pytest
from prejudice.errors import ConstraintError, ConstraintsErrors


def test_error():
    error = ConstraintError('test')
    assert error.message == 'test'
    assert error == ConstraintError('test')
    assert not error == 'test'

    with pytest.raises(AttributeError) as exc:
        error.message = 'I am immutable'


def test_errors():
    error1 = ConstraintError('test 1')
    error2 = ConstraintError('test 2')

    errors = ConstraintsErrors(error1, error2)
    assert len(errors) == 2
    assert errors == ConstraintsErrors(error1, error2)
    assert errors == [error1, error2]
    assert not errors == (error1, error2)

    assert errors.json() == (
        '''[{"message": "test 1"}, {"message": "test 2"}]'''
    )
