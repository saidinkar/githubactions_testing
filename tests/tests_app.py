'''This is a module-level docstring that describes the purpose of the test_app.py module.'''


from app import index


def test_index():
    '''This is a docstring that describes the test_index function.'''
    assert index() == "Hello Arch world!"
