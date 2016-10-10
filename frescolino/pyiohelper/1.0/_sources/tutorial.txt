Tutorial
========

This tutorial will guide you through the basic steps of using the ``iohelper`` module. 

Creating a :class:`.SerializerDispatch` instance
------------------------------------------------

To use the ``iohelper`` module, you must first create a :class:`.SerializerDispatch` instance. The instance is created with a specific encoding / decoding. Unless you want to use a custom encoding (see :ref:`custom`), you can use :mod:`.encoding.default`. This encoding handles common numpy and built-in types.

.. code :: python

    import fsc.iohelper as io
    IO_HANDLER = io.SerializerDispatch(io.encoding.default)
    
The task of the :class:`.SerializerDispatch` instance is to choose the correct serializer (possible options are :py:mod:`json`, :py:mod:`msgpack` and :py:mod:`pickle`), handle file operations and invoke the encoding and decoding functions.

Saving and loading
------------------

Having created the :class:`.SerializerDispatch` instance, you can use it to save data to a file:

.. code :: python

    IO_HANDLER = ...
    data = [1, 2, 3, 4]
    IO_HANDLER.save(data, 'filename.json')
    
To get the data back, you can use the :meth:`.load` method:
    
.. code :: python

    IO_HANDLER = ...
    result = IO_HANDLER.load('filename.json')

In both cases, the file format is automatically detected from the file ending. Possible file endings are ``.json`` for JSON files, ``.msgpack`` for msgpack, and ``.p`` or ``.pickle`` for pickle. The file endings are case insensitive, which means for example ``.JSON`` or ``.Json`` is equally valid.

You can also specify the serializer explicitly, by passing the ``json``, ``msgpack`` or ``pickle`` module as the ``serializer`` keyword argument.

.. code :: python

    import json
    import numpy as np
    
    IO_HANDLER = ...
    data = np.arange(4)
    IO_HANDLER.save(data, 'any_filename', serializer=json)
    
    result = IO_HANDLER.load('any_filename', serializer=json)

.. note :: If no serializer is given and the file ending is not understood, the ``json`` serializer will be used for saving data to avoid data loss. When loading, an error is raised instead to avoid accidentally loading corrupted data.

.. _custom:

Custom encoding / decoding
--------------------------

To define a custom encoding and decoding, an object which has two members ``encode`` and ``decode`` is needed. This object can be passed as the ``encoding`` argument to the :class:`.SerializerDispatch` constructor. 

The ``encode`` function should convert a given object into a JSON / msgpack - compatible type, and ``decode`` should do the inverse. When saving / loading, the functions are passed as the ``default`` (see :py:func:`json.dump`) and ``object_hook`` (see :py:func:`json.load`) parameters, respectively. The encoding and decoding functions are not used for the :py:mod:`pickle` serializer. Custom encodings for :py:mod:`pickle` are not currently supported.


.. code :: python

    import fsc.iohelper as io

    class Encoding:
        def encode(obj):
            ...
            
        def decode(obj):
            ...
            
    IO_HANDLER = io.SerializerDispatch(Encoding)

See the :mod:`.encoding.default` source code for a complete example implementation. 
