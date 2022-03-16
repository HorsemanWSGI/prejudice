from dataclasses import dataclass
from prejudice.errors import ConstraintError, ConstraintsErrors
from prejudice.validators import Or
from prejudice.utils import resolve_constraints
from prejudice.types import Predicate


@dataclass
class Document:
    id: str
    body: str = ''
    content_type: str = 'text/plain'


def non_empty_document(item):
    """Implementation of a validator/predicate
    """
    if not item.body:
        raise ConstraintError('Body is empty.')


def must_be_real_document(item):
    """Implementation of a validator/predicate
    """
    if item.id == 'test':
        raise ConstraintError('The item must not be a test document.')


class ContentType:

    def __init__(self, content_type):
        self.ct = content_type

    def __call__(self, item):
        if item.content_type != self.ct:
            raise ConstraintError(
                f'Expected {self.ct}, got {item.content_type}.')


class TestFunctionValidators:

    def test_single_resolution(self):
        document = Document(id='test', body='This is a test.')
        errors = resolve_constraints([non_empty_document], document)
        assert errors is None

        document = Document(id='test', body='')
        errors = resolve_constraints([non_empty_document], document)
        assert isinstance(errors, ConstraintsErrors)
        assert list(errors) == [ConstraintError('Body is empty.')]


    def test_multiple_resolution(self):
        document = Document(id='test', body='This is a test.')
        errors = resolve_constraints(
            [non_empty_document, must_be_real_document], document)
        assert list(errors) == [
            ConstraintError('The item must not be a test document.')
        ]

        document = Document(id='test')
        errors = resolve_constraints(
            [non_empty_document, must_be_real_document], document)
        assert list(errors) == [
            ConstraintError('Body is empty.'),
            ConstraintError('The item must not be a test document.')
        ]


class TestValidators:

    def test_single_resolution(self):
        document = Document(id='test', body='This is a test.')
        assert document.content_type == 'text/plain'
        errors = resolve_constraints([ContentType('text/plain')], document)
        assert errors is None

        errors = resolve_constraints([ContentType('text/html')], document)
        assert list(errors) == [
            ConstraintError('Expected text/html, got text/plain.')
        ]

    def test_multiple_resolution(self):
        document = Document(id='test', body='This is a test.')
        assert document.content_type == 'text/plain'
        errors = resolve_constraints([
            ContentType('text/plain'),
            must_be_real_document
        ], document)
        assert list(errors) == [
            ConstraintError('The item must not be a test document.')
        ]

        errors = resolve_constraints([
            ContentType('text/html'),
            must_be_real_document
        ], document)
        assert list(errors) == [
            ConstraintError('Expected text/html, got text/plain.'),
            ConstraintError('The item must not be a test document.')
        ]

        document = Document(
            id='not_test',
            body='<html></html>',
            content_type='text/html'
        )
        errors = resolve_constraints([
            ContentType('text/html'),
            must_be_real_document
        ], document)
        assert errors is None


class TestOr:

    def test_typing(self):
        import typing as t

        _or = Or()
        assert isinstance(_or, tuple)
        assert isinstance(_or, t.Callable)
        assert _or == tuple()

    def test_empty_or(self):
        _or = Or()
        assert _or() is None

    def test_basic_usage(self):
        import pytest

        _or = Or((ContentType('text/plain'), ContentType('text/html')))
        assert isinstance(_or, tuple)

        document = Document(id='test')
        assert _or(document) is None

        document = Document(id='test', content_type='application/json')
        with pytest.raises(ConstraintsErrors) as exc:
            _or(document)
            assert list(exc.value) == [
                ConstraintError('Expected text/plain, got application/json.'),
                ConstraintError('Expected text/html, got application/json.'),
            ]

    def test_stacked_or(self):
        import pytest

        _or = Or((
            ContentType('text/plain'),
            Or((ContentType('text/html'), non_empty_document))
        ))
        document = Document(id='test')
        assert _or(document) is None

        document = Document(id='test', content_type='application/json')
        with pytest.raises(ConstraintsErrors) as exc:
            _or(document)

        assert list(exc.value) == [
            ConstraintError('Expected text/plain, got application/json.'),
            ConstraintError('Expected text/html, got application/json.'),
            ConstraintError('Body is empty.'),
        ]

        _or = Or((
            ContentType('text/plain'),
            Or((
                Or((ContentType('text/html'), must_be_real_document)),
                non_empty_document))
            ))
        document = Document(id='123', content_type='application/json')
        assert _or(document) is None

        document = Document(id='test', content_type='application/json')
        with pytest.raises(ConstraintsErrors) as exc:
            _or(document)

        assert list(exc.value) == [
            ConstraintError('Expected text/plain, got application/json.'),
            ConstraintError('Expected text/html, got application/json.'),
            ConstraintError('The item must not be a test document.'),
            ConstraintError('Body is empty.'),
        ]

    def test_resolve_Or(self):
        _or = Or((
            ContentType('text/plain'),
            Or((ContentType('text/html'), non_empty_document))
        ))

        document = Document(id='test', content_type='application/json')
        errors = resolve_constraints(_or, document)
        assert errors == ConstraintsErrors(
            ConstraintError('Expected text/plain, got application/json.'),
            ConstraintError('Expected text/html, got application/json.'),
            ConstraintError('Body is empty.')
        )
