prejudice
*********

This package helps defining and creating small and reusable components
that can serve as guard or validation methods.


Example
=======

Below is an example of a validation on a content item.


.. code-block:: python

  from dataclasses import dataclass
  from prejudice.errors import ConstraintError
  from prejudice.validators import Or


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


  class ContentType:

      def __init__(self, content_type):
          self.ct = content_type

      def __call__(self, item):
          if item.content_type != self.ct:
              raise ConstraintError(
                  f'Expected {self.ct}, got {item.content_type}.')


    validator = Or((
        ContentType('text/plain'),
        Or((ContentType('text/html'), non_empty_document))
    ))
    document = Document(id='test', content_type='application/json')
    validator(document)  # raises ConstraintsErrors
