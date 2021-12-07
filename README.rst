==============================
Paint for Handwritten Dataset
==============================

Requirements
============

* Image Magick >= 6.0
* poetry

You can build the environment using poetry below:

.. code-block:: sh
   
    poetry install

You have to change `etc/ImageMagick-6/policy.xml`.

before change

.. code-block:: XML

    <policy domain="coder" rights="none" pattern="PS" />
    <policy domain="coder" rights="none" pattern="PDF" />

after

.. code-block:: XML

    <policy domain="coder" rights="read|write" pattern="PS" />
    <policy domain="coder" rights="read|write" pattern="PDF" />

How to Use
==========

.. code-block:: sh

    poetry run python3 paint/window.py --cls "あ"

To Do
======

* ImageMagickを使いたくない
