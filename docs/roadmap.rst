.. _roadmap:

==========================
Project Roadmap
==========================

OpenLEADR is under development. The current version is |release|.

Upcoming releases
-----------------

======= ================================== ====================
Version Main features                      Target timeframe
======= ================================== ====================
0.6.0   Implement XMPP transport           January 2020
1.0.0   Certification by OpenADR Alliance  T.B.A.
======= ================================== ====================


Changelog
---------

openleadr 0.5.16
~~~~~~~~~~~~~~~~

Released: 15 december 2020

Bug fixes:

- Various bug fixes surrounding report registration. If your handlers returned only None or some incompatible values, it should now be much more graceful and helpful about it.
- Some bug fixes surrounding the placement of the resourceID within the oadrRegisterReport messages.
- Fixed parsing datetimes that don't contain microseconds; it is now also compatible with datetimes that only provide milliseconds.


openleadr 0.5.15
~~~~~~~~~~~~~~~~

Released: 15 december 2020

Bug fixes:

- Restore Python 3.7 compatibility (got broken in 0.5.14)

New features:

- You can now use a future instead of a callback function or coroutine when adding an event. This allows you to add and event and await the response in a single place.
- You can now add events that don't require a response, and the VEN will no longer respond to events that don't expect a response. In this case, your on_event handler may still, but does not need to, return an opt status. The returned opt status will be ignored in that case.


openleadr 0.5.14
~~~~~~~~~~~~~~~~

Released: 15 december 2020

New features:

- Added support for a status callback to the server.add_raw_event method, just like the ``server.add_event`` method.

API changes:

- Removed the stale server.run() method and replaced it with a coroutine that does the same as ``server.run_async()``.

Bug fixes:

- Removed a naming inconsistency in the objects.ActivePeriod object.
- Silently cancel running tasks when stopping the client or server.
- Implemented the full duration regex for parsing timedeltas.
- Various improvements to the test suite and some stale code cleanup.

Other changes:

- Changed the way openleadr is packaged, dropped the setup-time inclusion of the VERSION file.
- OpenLEADR is now also available under the previous name pyopenadr. A new version of pyopenadr will be released in lockstep with new versions of openleadr. pyopenadr only contains an ``__init__`` file that does ``from openleadr import *``.

openleadr 0.5.13
~~~~~~~~~~~~~~~~

Released: 10 december 2020

New features:

- This version adds support for the oadrRequestEvent on the VTN side.

Bug fixes:

- Fixed a bug where messages from the VTN that did not contain an EiResponse field caused a KeyError in the VEN (#33).


openleadr 0.5.12
~~~~~~~~~~~~~~~~

Released: 10 december 2020

New features:

- Events now cycle through the correct 'far', 'near', 'active', 'completed'.
- The Client now implements the ``on_update_event handler``, so that you can catch these event updates separately from the regular event messages.
- Added support for the ramp_up_duration parameter on the ``server.add_event`` method.

Bug fixes:

- The OpenADRServer would block ``oadrPoll`` requests when no internal messages were available. This has been corrected.
- Some left-over ``print()`` statements have been removed.
- Nonce caching was badly broken in a previous version, this has now been fixed.



openleadr 0.5.11
~~~~~~~~~~~~~~~~

Released: 3 december 2020

New features:

- This update makes the list of Targets available as a dictionary of targets grouped by their type.
- You can now add Targets to events in multiple ways (``target``, ``targets``, and ``targets_by_type``).

Changes:

- The member names of the 'measurement' objects or dicts have been changed to be consistent everywhere:
    - item_name -> name
    - item_description -> description
    - item_units -> unit
    - si_scale_code -> scale
    This way, the parameters to client.add_report() are consistent with the Measurement object and the dicts that are passed around.
    Additionally, there is extra validation to prevent sending invalid measurements, and hints to correct any mistakes.


openleadr 0.5.10
~~~~~~~~~~~~~~~~

Released: 1 december 2020

Bug fixes:

- The on_created_event handler is now expected to receive the parameters (ven_id, event_id, opt_type). This was already in the docs, but not yet in the actual implementation. This has now been fixed.

openleadr 0.5.9
~~~~~~~~~~~~~~~

Released: 1 december 2020

New features:

- Added the ven fingerprint to the registration_info dict for the ``on_create_party_registration`` handler. This allows the VTN to verify the fingerprint upon registration, even when the VEN does not have a venID yet.

Changes:
- Converted the OpenADRServer.add_raw_event method to a normal (synchronous) method.

Bug fixes:
- The EiResponse.response_code would not always show up correctly, this is now fixed.

openleadr 0.5.8
~~~~~~~~~~~~~~~

Released: 30 november 2020

New features:

- Added the ``ven_id`` to the list of parameters for the ``on_register_report`` handler, so that this handler can know which VEN is registering reports
- Updated documentation to reflect the current API of OpenLEADR

openleadr 0.5.7
~~~~~~~~~~~~~~~

Released: 27 november 2020

Bugs fixed:

- Fixed a typo in the EventService.on_created_event placeholder function

openleadr 0.5.5
~~~~~~~~~~~~~~~

Released: 23 november 2020

New features:

- Message signing now uses the correct C14n algorithm, as required by OpenADR
- Preliminary VEN support for multiple events in one DistributeEvent message

openleadr 0.5.4
~~~~~~~~~~~~~~~

Released: 23 november 2020

New features:

- Preliminary support for TELEMETRY_STATUS reports
- Changed the server.add_event to be a normal function (not a coroutine), which allows you to call it from a synchronous function if needed.

openleadr 0.5.3
~~~~~~~~~~~~~~~

Released: 20 november 2020

New features:

- Support for custom units in Reports is back, and is now compliant with the XML Schema.
- Support for specifying the measurement (unit) in an EventSignal is added, and builds on the work of the report units.


openleadr 0.5.2
~~~~~~~~~~~~~~~

Released: 19 november 2020


Bug fixes:

- The 'full' report data collection mode now works correctly
- Various codestyle improvements and cleanup

Known issues:

- The support for out-of-schema measurements in repors has been removed, because they would not pass XML validation. We are exploring solutions to this problem. Track the progress here: `Issue #20 <https://github.com/OpenLEADR/openleadr-python/issues/20>`_

openleadr 0.5.1
~~~~~~~~~~~~~~~

Released: 19 november 2020

New features:

- When using SSL connections, the client will provide server side SSL certificates. The VTN will verify the fingerprint of these certificates against the known fingerprint for that ven. This should complete the VEN authentication process.


Bug fixes:

- Report messages now validate according to the XML schema. A few corrections were made to the templates from version 0.5.0.


Known issues:

- The support for out-of-schema measurements in repors has been removed, because they would not pass XML validation. We are exploring solutions to this problem. Track the progress here: `Issue #20 <https://github.com/OpenLEADR/openleadr-python/issues/20>`_


openleadr 0.5.0
~~~~~~~~~~~~~~~

Released: 16 november 2020

First release to pypi.org.

New features:

- This release implements reporting functionality into the client and the server. This is a major new area of functionality for OpenLEADR.

openleadr 0.4.0
~~~~~~~~~~~~~~~

Released: 16 november 2020

Only released to git.

New features:

- This release implements XML Message Signing for client and servers.

