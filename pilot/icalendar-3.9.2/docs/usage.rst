iCalendar package
=================

This package is used for parsing and generating iCalendar files following the
standard in RFC 2445.

It should be fully compliant, but it is possible to generate and parse invalid
files if you really want to.


File structure
--------------

An iCalendar file is a text file (utf-8) with a special format. Basically it
consists of content lines.

Each content line defines a property that has 3 parts (name, parameters,
values). Parameters are optional.

A simple content line with only name and value could look like this::

  BEGIN:VCALENDAR

A content line with parameters can look like this::

  ATTENDEE;CN=Max Rasmussen;ROLE=REQ-PARTICIPANT:MAILTO:example@example.com

And the parts are::

  Name:   ATTENDEE
  Params: CN=Max Rasmussen;ROLE=REQ-PARTICIPANT
  Value:  MAILTO:example@example.com

Long content lines are usually "folded" to less than 75 character, but the
package takes care of that.


Overview
--------

On a higher level iCalendar files consists of components. Components can have
sub components.

The root component is the VCALENDAR::

  BEGIN:VCALENDAR
  ... vcalendar properties ...
  END:VCALENDAR

The most frequent subcomponent to a VCALENDAR is a VEVENT. They are
nested like this::

  BEGIN:VCALENDAR
  ... vcalendar properties ...
  BEGIN:VEVENT
  ... vevent properties ...
  END:VEVENT
    END:VCALENDAR

Inside the components there are properties with values. The values
have special types. like integer, text, datetime etc. These values are
encoded in a special text format in an iCalendar file.

There are methods for converting to and from these encodings in the package.

These are the most important imports::

  >>> from icalendar import Calendar, Event


Components
----------

Components are like (Case Insensitive) dicts. So if you want to set a property
you do it like this. The calendar is a component::

  >>> cal = Calendar()
  >>> cal['dtstart'] = '20050404T080000'
  >>> cal['summary'] = 'Python meeting about calendaring'
  >>> for k,v in cal.items():
  ...     k,v
  (u'DTSTART', '20050404T080000')
  (u'SUMMARY', 'Python meeting about calendaring')

NOTE: the recommended way to add components to the calendar is to use
create the subcomponent and add it via Calendar.add! The example above adds a
string, but not a vText component.


You can generate a string for a file with the to_ical() method::

  >>> cal.to_ical()
  'BEGIN:VCALENDAR\r\nDTSTART:20050404T080000\r\nSUMMARY:Python meeting about calendaring\r\nEND:VCALENDAR\r\n'

The rendered view is easier to read::

  BEGIN:VCALENDAR
  DTSTART:20050404T080000
  SUMMARY:Python meeting about calendaring
  END:VCALENDAR

So, let's define a function so we can easily display to_ical() output::

  >>> def display(cal):
  ...    return cal.to_ical().replace('\r\n', '\n').strip()

You can set multiple properties like this::

  >>> cal = Calendar()
  >>> cal['attendee'] = ['MAILTO:maxm@mxm.dk','MAILTO:test@example.com']
  >>> print display(cal)
  BEGIN:VCALENDAR
  ATTENDEE:MAILTO:maxm@mxm.dk
  ATTENDEE:MAILTO:test@example.com
  END:VCALENDAR

If you don't want to care about whether a property value is a list or
a single value, just use the add() method. It will automatically
convert the property to a list of values if more than one value is
added. Here is an example::

  >>> cal = Calendar()
  >>> cal.add('attendee', 'MAILTO:maxm@mxm.dk')
  >>> cal.add('attendee', 'MAILTO:test@example.com')
  >>> print display(cal)
  BEGIN:VCALENDAR
  ATTENDEE:MAILTO:maxm@mxm.dk
  ATTENDEE:MAILTO:test@example.com
  END:VCALENDAR

Note: this version doesn't check for compliance, so you should look in
the RFC 2445 spec for legal properties for each component, or look in
the icalendar/calendar.py file, where it is at least defined for each
component.


Subcomponents
-------------

Any component can have subcomponents. Eg. inside a calendar there can
be events.  They can be arbitrarily nested. First by making a new
component::

  >>> event = Event()
  >>> event['uid'] = '42'
  >>> event['dtstart'] = '20050404T080000'

And then appending it to a "parent"::

  >>> cal.add_component(event)
  >>> print display(cal)
  BEGIN:VCALENDAR
  ATTENDEE:MAILTO:maxm@mxm.dk
  ATTENDEE:MAILTO:test@example.com
  BEGIN:VEVENT
  DTSTART:20050404T080000
  UID:42
  END:VEVENT
  END:VCALENDAR

Subcomponents are appended to the subcomponents property on the component::

  >>> cal.subcomponents
  [VEVENT({'DTSTART': '20050404T080000', 'UID': '42'})]


Value types
-----------

Property values are utf-8 encoded strings.

This is impractical if you want to use the data for further
computation. Eg. the datetime format looks like this:
'20050404T080000'. But the package makes it simple to Parse and
generate iCalendar formatted strings.

Basically you can make the add() method do the thinking, or you can do it
yourself.

To add a datetime value, you can use Pythons built in datetime types,
and the set the encode parameter to true, and it will convert to the
type defined in the spec::

  >>> from datetime import datetime
  >>> cal.add('dtstart', datetime(2005,4,4,8,0,0))
  >>> cal['dtstart'].to_ical()
  '20050404T080000'

If that doesn't work satisfactorily for some reason, you can also do it
manually.

In 'icalendar.prop', all the iCalendar data types are defined. Each
type has a class that can parse and encode the type.

So if you want to do it manually::

  >>> from icalendar import vDatetime
  >>> now = datetime(2005,4,4,8,0,0)
  >>> vDatetime(now).to_ical()
  '20050404T080000'

So the drill is to initialise the object with a python built in type,
and then call the "to_ical()" method on the object. That will return an
ical encoded string.

You can do it the other way around too. To parse an encoded string, just call
the "from_ical()" method, and it will return an instance of the corresponding
Python type::

  >>> vDatetime.from_ical('20050404T080000')
  datetime.datetime(2005, 4, 4, 8, 0)

  >>> dt = vDatetime.from_ical('20050404T080000Z')
  >>> repr(dt)[:62]
  'datetime.datetime(2005, 4, 4, 8, 0, tzinfo=<UTC>)'

You can also choose to use the decoded() method, which will return a decoded
value directly::

  >>> cal = Calendar()
  >>> cal.add('dtstart', datetime(2005,4,4,8,0,0))
  >>> cal['dtstart'].to_ical()
  '20050404T080000'
  >>> cal.decoded('dtstart')
  datetime.datetime(2005, 4, 4, 8, 0)


Property parameters
-------------------

Property parameters are automatically added, depending on the input value. For
example, for date/time related properties, the value type and timezone
identifier (if applicable) are automatically added here::

    >>> event = Event()
    >>> event.add('dtstart', datetime(2010, 10, 10, 10, 0, 0,
    ...                               tzinfo=pytz.timezone("Europe/Vienna")))

    >>> lines = event.to_ical().splitlines()
    >>> self.assertTrue(
    ...     b"DTSTART;TZID=Europe/Vienna;VALUE=DATE-TIME:20101010T100000"
    ...     in lines)


You can also add arbitrary property parameters by passing a parameters
dictionary to the add method like so::

    >>> event = Event()
    >>> event.add('X-TEST-PROP', 'tryout.',
    ....          parameters={'prop1': 'val1', 'prop2': 'val2'})
    >>> lines = event.to_ical().splitlines()
    >>> self.assertTrue(b"X-TEST-PROP;PROP1=val1;PROP2=val2:tryout." in lines)


Example
-------

Here is an example generating a complete iCal calendar file with a
single event that can be loaded into the Mozilla calendar

Init the calendar::

  >>> cal = Calendar()
  >>> from datetime import datetime

Some properties are required to be compliant::

  >>> cal.add('prodid', '-//My calendar product//mxm.dk//')
  >>> cal.add('version', '2.0')

We need at least one subcomponent for a calendar to be compliant::

  >>> import pytz
  >>> event = Event()
  >>> event.add('summary', 'Python meeting about calendaring')
  >>> event.add('dtstart', datetime(2005,4,4,8,0,0,tzinfo=pytz.utc))
  >>> event.add('dtend', datetime(2005,4,4,10,0,0,tzinfo=pytz.utc))
  >>> event.add('dtstamp', datetime(2005,4,4,0,10,0,tzinfo=pytz.utc))

A property with parameters. Notice that they are an attribute on the value::

  >>> from icalendar import vCalAddress, vText
  >>> organizer = vCalAddress('MAILTO:noone@example.com')

Automatic encoding is not yet implemented for parameter values, so you
must use the 'v*' types you can import from the icalendar package
(they're defined in ``icalendar.prop``)::

  >>> organizer.params['cn'] = vText('Max Rasmussen')
  >>> organizer.params['role'] = vText('CHAIR')
  >>> event['organizer'] = organizer
  >>> event['location'] = vText('Odense, Denmark')

  >>> event['uid'] = '20050115T101010/27346262376@mxm.dk'
  >>> event.add('priority', 5)

  >>> attendee = vCalAddress('MAILTO:maxm@example.com')
  >>> attendee.params['cn'] = vText('Max Rasmussen')
  >>> attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
  >>> event.add('attendee', attendee, encode=0)

  >>> attendee = vCalAddress('MAILTO:the-dude@example.com')
  >>> attendee.params['cn'] = vText('The Dude')
  >>> attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
  >>> event.add('attendee', attendee, encode=0)

Add the event to the calendar::

  >>> cal.add_component(event)

Write to disk::

  >>> import tempfile, os
  >>> directory = tempfile.mkdtemp()
  >>> f = open(os.path.join(directory, 'example.ics'), 'wb')
  >>> f.write(cal.to_ical())
  >>> f.close()


More documentation
==================

Have a look at the tests of this package to get more examples.
All modules and classes docstrings, which document how they work.
