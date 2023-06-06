Flaskr
======

The basic blog app built in the Flask `tutorial`_.

.. _tutorial: https://flask.palletsprojects.com/tutorial/


Install
-------

Create a virtualenv and activate it::

    $ python3 -m virtualenv venv
    $ source venv/bin/activate

Or on Windows cmd::

    $ py -3 -m venv venv
    $ venv\Scripts\activate.bat

Install dependencies::

    $ pip install -r requirements.txt

Run
---

.. code-block:: text

    $ flask --app flaskr init-db
    $ flask --app flaskr run --debug

Open http://127.0.0.1:5000 in a browser.


Test
----

::

    $ python3 -m pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html     # open htmlcov/index.html in a browser
