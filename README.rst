Hispadocs
#########
Hispanics is a utility for creating odt documents from templates. Features include:

* Join multiple odt documents into one.
* Jinja2 template language (a.k.a, ``{{ variable }}``).

Install
=======
If you have pip installed (¡**Python2**!), you can use:

.. code-block:: bash

    $ pip install hispadocs

Usage
=====
Imagine you have 3 odt documents and you want to join them. Also, you have variables in the files. For example::

    agreement.odt
    -------------
    From {{ company_name }} to {{ client }} with telephone {{ telephone }}.

    Thank you very much for contracting our services.
    ...

You need the first a **configuration file**. You can call it ``config.yml``, for example:

.. code-block:: yaml

    inputs:
      - cover.odt
      - index.odt
      - agreement.odt
    output: out.odt
    vars:
      company_name: Hispasec Sistemas
      client: Pepe García
      telephone: 600000000

The input odt files must be in the same folder as the configuration file. Now you can run:

.. code-block:: bash
    hispadocs generate config.yml
