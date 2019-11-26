Tutorial
========

The :meth:`export() <fsc.export.export>` decorator can be used on any object which should be added to the module's ``__all__``.

.. code:: python

    # in module test

    from fsc.export import export

    @export
    class Test:
        pass

    @export
    def test():
        pass

To test whether all exported objects have a non-zero docstring, call the :meth:`test_doc() <fsc.export.test_doc>` method before importing the module.

.. code:: python

    import fsc.export
    fsc.export.test_doc()

    import test # raises AssertionError
