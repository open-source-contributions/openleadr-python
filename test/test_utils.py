from openleadr import utils, objects
from dataclasses import dataclass
import pytest
from datetime import datetime, timezone, timedelta
from collections import deque

@dataclass
class dc:
    a: int = 2

def test_hasmember():
    obj = {'a': 1}
    assert utils.hasmember(obj, 'a') == True
    assert utils.hasmember(obj, 'b') == False

    obj = dc()
    assert utils.hasmember(obj, 'a') == True
    assert utils.hasmember(obj, 'b') == False

def test_getmember():
    obj = {'a': 1}
    assert utils.getmember(obj, 'a') == 1

    obj = dc()
    assert utils.getmember(obj, 'a') == 2

def test_setmember():
    obj = {'a': 1}
    utils.setmember(obj, 'a', 10)
    assert utils.getmember(obj, 'a') == 10

    obj = dc()
    utils.setmember(obj, 'a', 10)
    assert utils.getmember(obj, 'a') == 10

@pytest.mark.asyncio
async def test_delayed_call_with_func():
    async def myfunc():
        pass
    await utils.delayed_call(myfunc, delay=0.1)

@pytest.mark.asyncio
async def test_delayed_call_with_coro():
    async def mycoro():
        pass
    await utils.delayed_call(mycoro(), delay=0.1)

@pytest.mark.asyncio
async def test_delayed_call_with_coro_func():
    async def mycoro():
        pass
    await utils.delayed_call(mycoro, delay=0.1)

def test_determine_event_status_completed():
    active_period = {'dtstart': datetime.now(timezone.utc) - timedelta(seconds=10),
                     'duration': timedelta(seconds=5)}
    assert utils.determine_event_status(active_period) == 'completed'

def test_determine_event_status_active():
    active_period = {'dtstart': datetime.now(timezone.utc) - timedelta(seconds=10),
                     'duration': timedelta(seconds=15)}
    assert utils.determine_event_status(active_period) == 'active'

def test_determine_event_status_near():
    active_period = {'dtstart': datetime.now(timezone.utc) + timedelta(seconds=3),
                     'duration': timedelta(seconds=5),
                     'ramp_up_duration': timedelta(seconds=5)}
    assert utils.determine_event_status(active_period) == 'near'

def test_determine_event_status_far():
    active_period = {'dtstart': datetime.now(timezone.utc) + timedelta(seconds=10),
                     'duration': timedelta(seconds=5)}
    assert utils.determine_event_status(active_period) == 'far'

def test_determine_event_status_far_with_ramp_up():
    active_period = {'dtstart': datetime.now(timezone.utc) + timedelta(seconds=10),
                     'duration': timedelta(seconds=5),
                     'ramp_up_duration': timedelta(seconds=5)}
    assert utils.determine_event_status(active_period) == 'far'

def test_get_active_period_from_intervals():
    now = datetime.now(timezone.utc)
    intervals=[{'dtstart': now,
                'duration': timedelta(seconds=5)},
                {'dtstart': now + timedelta(seconds=5),
                'duration': timedelta(seconds=5)}]
    assert utils.get_active_period_from_intervals(intervals) == {'dtstart': now,
                                                                       'duration': timedelta(seconds=10)}

    intervals=[objects.Interval(dtstart=now,
                                duration=timedelta(seconds=5),
                                signal_payload=1),
               objects.Interval(dtstart=now + timedelta(seconds=5),
                                duration=timedelta(seconds=5),
                                signal_payload=2)]
    assert utils.get_active_period_from_intervals(intervals) == {'dtstart': now,
                                                                 'duration': timedelta(seconds=10)}

    assert utils.get_active_period_from_intervals(intervals, False) == objects.ActivePeriod(dtstart=now,
                                                                                            duration=timedelta(seconds=10))

def test_cron_config():
    assert utils.cron_config(timedelta(seconds=5)) == {'second': '*/5', 'minute': '*', 'hour': '*'}
    assert utils.cron_config(timedelta(minutes=1)) == {'second': '0', 'minute': '*/1', 'hour': '*'}
    assert utils.cron_config(timedelta(minutes=5)) == {'second': '0', 'minute': '*/5', 'hour': '*'}
    assert utils.cron_config(timedelta(hours=1)) == {'second': '0', 'minute': '0', 'hour': '*/1'}
    assert utils.cron_config(timedelta(hours=2)) == {'second': '0', 'minute': '0', 'hour': '*/2'}
    assert utils.cron_config(timedelta(hours=25)) == {'second': '0', 'minute': '0', 'hour': '0'}
    assert utils.cron_config(timedelta(seconds=10), randomize_seconds=True) == {'second': '*/10',
                                                                                'minute': '*',
                                                                                'hour': '*',
                                                                                'jitter': 1}

def test_get_event_from_deque():
    d = deque()
    now = datetime.now(timezone.utc)
    event1 = objects.Event(event_descriptor=objects.EventDescriptor(event_id='event123',
                                                                    event_status='far',
                                                                    modification_number='1',
                                                                    market_context='http://marketcontext01'),
                           event_signals=[objects.EventSignal(signal_name='simple',
                                                              signal_type='level',
                                                              signal_id=utils.generate_id(),
                                                              intervals=[objects.Interval(dtstart=now,
                                                                                          duration=timedelta(minutes=10),
                                                                                          signal_payload=1)])],
                            targets=[{'ven_id': 'ven123'}])
    msg_one = {'message': 'one'}
    msg_two = {'message': 'two'}
    msg_three = {'message': 'three'}
    event2 = objects.Event(event_descriptor=objects.EventDescriptor(event_id='event123',
                                                                    event_status='far',
                                                                    modification_number='1',
                                                                    market_context='http://marketcontext01'),
                           event_signals=[objects.EventSignal(signal_name='simple',
                                                              signal_type='level',
                                                              signal_id=utils.generate_id(),
                                                              intervals=[objects.Interval(dtstart=now,
                                                                                          duration=timedelta(minutes=10),
                                                                                          signal_payload=1)])],
                            targets=[{'ven_id': 'ven123'}])

    d.append(event1)
    d.append(msg_one)
    d.append(msg_two)
    d.append(msg_three)
    d.append(event2)
    assert utils.get_next_event_from_deque(d) is event1
    assert utils.get_next_event_from_deque(d) is event2
    assert utils.get_next_event_from_deque(d) is None
    assert utils.get_next_event_from_deque(d) is None
    assert len(d) == 3
    assert d.popleft() is msg_one
    assert d.popleft() is msg_two
    assert d.popleft() is msg_three
    assert len(d) == 0
    assert utils.get_next_event_from_deque(d) is None


def test_validate_report_measurement_dict_missing_items(caplog):
    measurement = {'name': 'rainbows'}
    with pytest.raises(ValueError) as err:
        utils.validate_report_measurement_dict(measurement)
    assert str(err.value) == (f"The measurement dict must contain the following keys: "
                              "'name', 'description', 'unit'. Please correct this.")

def test_validate_report_measurement_dict_invalid_name(caplog):
    measurement = {'name': 'rainbows',
                   'unit': 'B',
                   'description': 'Rainbows'}
    utils.validate_report_measurement_dict(measurement)
    assert measurement['name'] == 'customUnit'
    assert (f"You provided a measurement with an unknown name rainbows. "
            "This was corrected to 'customUnit'. Please correct this in your "
            "report definition.") in caplog.messages


def test_validate_report_measurement_dict_invalid_unit():
    with pytest.raises(ValueError) as err:
        measurement = {'name': 'current',
                       'unit': 'B',
                       'description': 'Current'}
        utils.validate_report_measurement_dict(measurement)
    assert str(err.value) == (f"The unit 'B' is not acceptable for measurement 'current'. Allowed "
                              f"units are: 'A'.")


def test_validate_report_measurement_dict_invalid_description(caplog):
    with pytest.raises(ValueError) as err:
        measurement = {'name': 'current',
                       'unit': 'A',
                       'description': 'something'}
        utils.validate_report_measurement_dict(measurement)

    str(err.value) ==  (f"The measurement's description 'something' "
                        f"did not match the expected description for this type "
                        f" ('Current'). Please correct this, or use "
                        "'customUnit' as the name.")

def test_validate_report_measurement_dict_invalid_description_case(caplog):
    measurement = {'name': 'current',
                   'unit': 'A',
                   'description': 'CURRENT'}
    utils.validate_report_measurement_dict(measurement)
    assert measurement['description'] == 'Current'

    assert (f"The description for the measurement with name 'current' "
            f"was not in the correct case; you provided 'CURRENT' but "
            f"it should be 'Current'. "
            "This was automatically corrected.") in caplog.messages


def test_validate_report_measurement_dict_missing_power_attributes(caplog):
    with pytest.raises(ValueError) as err:
        measurement = {'name': 'powerReal',
                       'description': 'RealPower',
                       'unit': 'W'}
        utils.validate_report_measurement_dict(measurement)
    assert str(err.value) == ("A 'power' related measurement must contain a "
                              "'power_attributes' section that contains the following "
                              "keys: 'voltage' (int), 'ac' (boolean), 'hertz' (int)")


def test_validate_report_measurement_dict_invalid_power_attributes(caplog):
    with pytest.raises(ValueError) as err:
        measurement = {'name': 'powerReal',
                       'description': 'RealPower',
                       'unit': 'W',
                       'power_attributes': {'a': 123}}
        utils.validate_report_measurement_dict(measurement)
    assert str(err.value) == ("The power_attributes of the measurement must contain the "
                              "following keys: 'voltage' (int), 'ac' (bool), 'hertz' (int).")

def test_ungroup_target_by_type_with_single_str():
    targets_by_type = {'ven_id': 'ven123'}
    targets = utils.ungroup_targets_by_type(targets_by_type)
    assert targets == [{'ven_id': 'ven123'}]

def test_find_by_with_dict():
    search_dict = {'one': {'a': 123, 'b': 456},
                   'two': {'a': 321, 'b': 654}}
    result = utils.find_by(search_dict, 'a', 123)
    assert result == {'a': 123, 'b': 456}

def test_find_by_with_missing_member():
    search_list = [{'a': 123, 'b': 456},
                   {'a': 321, 'b': 654, 'c': 1000}]
    result = utils.find_by(search_list, 'c', 1000)
    assert result == {'a': 321, 'b': 654, 'c': 1000}

def test_ensure_str():
    assert utils.ensure_str("Hello") == "Hello"
    assert utils.ensure_str(b"Hello") == "Hello"
    assert utils.ensure_str(None) is None
    with pytest.raises(TypeError) as err:
        utils.ensure_str(1)
    assert str(err.value) == "Must be bytes or str"

def test_ensure_bytes():
    assert utils.ensure_bytes("Hello") == b"Hello"
    assert utils.ensure_bytes(b"Hello") == b"Hello"
    assert utils.ensure_bytes(None) is None
    with pytest.raises(TypeError) as err:
        utils.ensure_bytes(1)
    assert str(err.value) == "Must be bytes or str"

def test_booleanformat():
    assert utils.booleanformat("true") == "true"
    assert utils.booleanformat("false") == "false"
    assert utils.booleanformat(True) == "true"
    assert utils.booleanformat(False) == "false"
    with pytest.raises(ValueError) as err:
        assert utils.booleanformat(123)
    assert str(err.value) == "A boolean value must be provided, not 123."

def test_parse_duration():
    assert utils.parse_duration("PT1M") == timedelta(minutes=1)
    assert utils.parse_duration("PT1M5S") == timedelta(minutes=1, seconds=5)
    assert utils.parse_duration("PT1H5M10S") == timedelta(hours=1, minutes=5, seconds=10)
    assert utils.parse_duration("P1DT1H5M10S") == timedelta(days=1, hours=1, minutes=5, seconds=10)
    assert utils.parse_duration("P1M") == timedelta(days=30)
    assert utils.parse_duration("-P1M") == timedelta(days=-30)
    assert utils.parse_duration("2W") == timedelta(days=14)
    with pytest.raises(ValueError) as err:
        utils.parse_duration("Hello")
    assert str(err.value) == f"The duration 'Hello' did not match the requested format"

def test_parse_datetime():
    assert utils.parse_datetime("2020-12-15T11:29:34Z") == datetime(2020, 12, 15, 11, 29, 34, tzinfo=timezone.utc)
    assert utils.parse_datetime("2020-12-15T11:29:34.123456Z") == datetime(2020, 12, 15, 11, 29, 34, 123456, tzinfo=timezone.utc)
    assert utils.parse_datetime("2020-12-15T11:29:34.123Z") == datetime(2020, 12, 15, 11, 29, 34, 123000, tzinfo=timezone.utc)
    assert utils.parse_datetime("2020-12-15T11:29:34.123456789Z") == datetime(2020, 12, 15, 11, 29, 34, 123456, tzinfo=timezone.utc)
