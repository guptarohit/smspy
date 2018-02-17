.. -*-restructuredtext-*-

SMSpy
=====
A minimalistic python wrapper for sending free sms via website `way2sms <http://www.way2sms.com>`_.

.. image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
    :target: https://www.python.org/


Installation
------------

::

    $ pip install -U git+git://github.com/guptarohit/smspy.git

Usage
-----


Send SMS
^^^^^^^^

.. code:: python

    from smspy import Way2sms

    w2s = Way2sms()

    w2s.login(USERNAME, PASSWORD)

    w2s.send(MOBILE_NO, MSG)

    w2s.logout()


Schedule SMS
^^^^^^^^^^^^

.. code:: python

    from smspy import Way2sms

    w2s = Way2sms()

    w2s.login(USERNAME, PASSWORD)

    w2s.schedule(MOBILE_NO, MSG, DATE, TIME)
    # DATE should be in format DD/MM/YYYY and TIME in 24h HH:mm

    w2s.logout()


Check History of sent messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from smspy import Way2sms

    w2s = Way2sms()

    w2s.login(USERNAME, PASSWORD)

    headers, data = w2s.history(DATE)
    # DATE should be in format DD/MM/YYYY

    print(headers, data)

    w2s.logout()


Check Scheduled messages
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from smspy import Way2sms

    w2s = Way2sms()

    w2s.login(USERNAME, PASSWORD)

    headers, data = w2s.scheduled_messages(DATE)
    # DATE should be in format DD/MM/YYYY

    print(headers, data)

    w2s.logout()


Check Quota left
^^^^^^^^^^^^^^^^

.. code:: python

    from smspy import Way2sms

    w2s = Way2sms()

    w2s.login(USERNAME, PASSWORD)

    msgs_remaining=w2s.quota_left()

    print(msgs_remaining)

    w2s.logout()


Contributing
------------

Feel free to make a pull request! :octocat:
