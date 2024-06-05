# Tutorial - Continuous Line / Fly Scan
In this tutorial, we will show you how to write a continuous line fly scan using a BEC server plugin. This tutorial assumes that you have already set up the BEC server and that you have a basic understanding of the scan structure in the BEC server. If not, please refer to the [scan documentation](#developer.scans).

## Desired Outcome
We want to write a fly scan that moves a motor from one position to another at a constant speed. Throughout the scan, we want to send triggers as fast as possible (respecting the requested exposure time). Once the motor reaches the end position, we want to stop the scan.

## Step 1: Create a New Scan
Let's start by creating a new scan file in the `scans` directory of our plugin repository and name it tutorial_fly_scan_cont_line.py. We will start by importing the necessary modules and defining the scan class. Since we are writing a fly scan, we want to inherit from a FlyScan base class. In our case, we will inherit from the `AsyncFlyScanBase` class as our flyer will not be in charge of synchronizing the data collection.

```python
import numpy as np

from bec_lib.device import DeviceBase
from bec_server.scan_server.scans import AsyncFlyScanBase

class TutorialFlyScanContLine(AsyncFlyScanBase):
    scan_name = "tutorial_fly_scan_cont_line"
```

To make the scan available to the BEC server, we need to add it the `__init__.py` file in the scans directory. To this end, add the following line to the `__init__.py` file:

```python
from .tutorial_fly_scan_cont_line import TutorialFlyScanContLine
```

## Step 2: Define the Scan Parameters
Next, we need to define the scan parameters. In our case, we want to pass in the following parameters:
- `motor`: The motor to move during the scan. This should be a `DeviceBase` object, i.e. any device that inherits from the `DeviceBase` class.
- `start`: The starting position of the motor. This should be a float.
- `end`: The ending position of the motor. This should be a float.
- `exp_time`: The exposure time for each trigger. This should be a float.
- `relative`: A boolean flag indicating whether the end position is relative to the start position. If `True`, the end position will be added to the start position. If `False`, the end position will be used as an absolute position. This should be a boolean.

With this in mind, we can define the `__init__` method of our scan class as follows:

```python
    def __init__(
        self,
        motor: DeviceBase,
        start: float,
        stop: float,
        exp_time: float = 0,
        relative: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.motor = motor
        self.start = start
        self.stop = stop
        self.exp_time = exp_time
        self.relative = relative
```

Here, the `**kwargs` parameter allows us to pass additional keyword arguments to the base class. This is important as the base class may require additional parameters that we do not need to define in our scan class. After initializing the base class (FlyScanBase) using `super().__init__(**kwargs)`, we store the motor, start, stop, exp_time, and relative parameters as attributes of the scan class.

Let's also add a proper doc string for the users of our scan:

```python 
    def __init__(
        self,
        motor: DeviceBase,
        start: float,
        stop: float,
        exp_time: float = 0,
        relative: bool = False,
        **kwargs,
    ):
        """
        A continuous line fly scan. Use this scan if you want to move a motor continuously from start to stop position whilst acquiring data as fast as possible (respecting the exposure time). The scan will stop automatically when the motor reaches the end position.

        Args:
            motor (DeviceBase): motor to move continuously from start to stop position
            start (float): start position
            stop (float): stop position
            exp_time (float): exposure time in seconds. Default is 0.
            relative (bool): if True, the motor will be moved relative to its current position. Default is False.

        Returns:
            ScanReport

        Examples:
            >>> scans.tutorial_cont_line_fly_scan(dev.sam_rot, 0, 180, exp_time=0.1)

        """
        super().__init__(**kwargs)
        self.motor = motor
        self.start = start
        self.stop = stop
        self.exp_time = exp_time
        self.relative = relative
```

## Step 3: Prepare the positions
Our scan should move the motor from the start position to the stop position at a constant speed. To achieve this, we need to override the `prepare_positions` method:

```python
    def prepare_positions(self):
        self.positions = np.array([[self.start], [self.stop]])
        self.num_pos = None
        yield from self._set_position_offset()
```

By using `self._set_position_offset()`, we ensure that the motor is moved to the correct position before starting the scan, respecting the relative flag.

## Step 4: Define the scan logic
Next, we need to define the scan logic. In our case, the following steps are required and can be built upon the [scan stubs](#developer.scans.scan_stubs) provided by the BEC server:
- Move the motor to the start position. This can be achieved by using the [`set_and_wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.set_and_wait) method. 
- Send the flyer on its way to the defined stop position. This can be achieved by using the [`set_with_response`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.set_with_response) method.
- Wait for the trigger to complete. This can be achieved by using the [`wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.wait) method.
- Read out all devices on readout priority "monitored". This can be achieved by using the [`read_and_wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.read_and_wait) method, using the group "primary". 
- Check if the flyer has reached the stop position. This can be achieved by using the [`request_is_completed`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.request_is_completed) method.

Let's build the method accordingly:

```python
    def scan_core(self):
        # move the motor to the start position
        yield from self.stubs.set_and_wait(device=[self.motor], positions=self.positions[0])

        # start the flyer
        flyer_request = yield from self.stubs.set_with_response(device=self.motor, value=self.positions[1][0])


        while True:
            # send a trigger
            yield from self.stubs.trigger(group="trigger", point_id=self.point_id)
            # wait for the trigger to complete
            yield from self.stubs.wait(
                wait_type="trigger", group="trigger", wait_time=self.exp_time
            )
            # read the data
            yield from self.stubs.read_and_wait(
                group="primary", wait_group="readout_primary", point_id=self.point_id
            )

            if self.stubs.request_is_completed(flyer_request):
                # stop the scan if the motor has reached the stop position
                break

            # increase the point id
            self.point_id += 1
```

## Step 5: Finalize the scan
Finally, we need to define the `finalize` method to clean up after the scan is completed. As we did not define the `num_pos` attribute in the `prepare_positions` method, we need to calculate it here:

```python
    def finalize(self):
        yield from super().finalize()
        self.num_pos = self.point_id + 1
```

This will ensure that the scan report contains the correct number of positions.

Your scan class is now complete and should look like this:

```python
import numpy as np

from bec_lib.device import DeviceBase
from bec_server.scan_server.scans import AsyncFlyScanBase


class TutorialFlyScanContLine(AsyncFlyScanBase):
    scan_name = "tutorial_cont_line_fly_scan"

    def __init__(
        self,
        motor: DeviceBase,
        start: float,
        stop: float,
        exp_time: float = 0,
        relative: bool = False,
        **kwargs,
    ):
        """
        A continuous line fly scan. Use this scan if you want to move a motor continuously from start to stop position whilst
        acquiring data as fast as possible (respecting the exposure time). The scan will stop automatically when the motor
        reaches the end position.

        Args:
            motor (DeviceBase): motor to move continuously from start to stop position
            start (float): start position
            stop (float): stop position
            exp_time (float): exposure time in seconds. Default is 0.
            relative (bool): if True, the motor will be moved relative to its current position. Default is False.

        Returns:
            ScanReport

        Examples:
            >>> scans.tutorial_cont_line_fly_scan(dev.sam_rot, 0, 180, exp_time=0.1)

        """
        super().__init__(**kwargs)
        self.motor = motor
        self.start = start
        self.stop = stop
        self.exp_time = exp_time
        self.relative = relative

    def prepare_positions(self):
        self.positions = np.array([[self.start], [self.stop]])
        self.num_pos = None
        yield from self._set_position_offset()

    def scan_core(self):
        # move the motor to the start position
        yield from self.stubs.set_and_wait(device=[self.motor], positions=self.positions[0])

        # start the flyer
        flyer_request = yield from self.stubs.set_with_response(device=self.motor, value=self.positions[1][0])


        while True:
            # send a trigger
            yield from self.stubs.trigger(group="trigger", point_id=self.point_id)
            # wait for the trigger to complete
            yield from self.stubs.wait(
                wait_type="trigger", group="trigger", wait_time=self.exp_time
            )
            # read the data
            yield from self.stubs.read_and_wait(
                group="primary", wait_group="readout_primary", point_id=self.point_id
            )

            if self.stubs.request_is_completed(flyer_request):
                # stop the scan if the motor has reached the stop position
                break

            # increase the point id
            self.point_id += 1

    def finalize(self):
        yield from super().finalize()
        self.num_pos = self.point_id + 1
```

Once you have saved the file, restart the BEC server and the client. You should now be able to see your new scan showing up as `tutorial_fly_scan_cont_line` within `scans.<tab>`.

## Step 6: (Optional) Test the scan
Testing the scan is crucial to ensure that the scan works as expected, even if the components of BEC change. The architecture of scans in BEC allows for easy testing as the scan logic is separated from the hardware control. As a result, we only need to ensure that the scan logic is correct. This can be achieved by ensuring that the correct instructions are sent to the scan worker. 

Let's create a new test file in the `tests/tests_scans` directory of our plugin repository and name it `test_tutorial_fly_scan_cont_line.py`. 

```{important}
In BEC, we are relying on the `pytest` package for testing. Therefore, all test files must be prefixed with `test_` to be picked up by the test runner.
Similarly, any file that should not be picked up by the test runner must not be prefixed with `test_`.
```

We will start by importing the necessary modules and defining the test class. We will then write a test that checks if the scan worker receives the correct instructions.

```python
from unittest import mock
from bec_server.device_server.tests.utils import DMMock
from <beamline_repo>.scans import TutorialFlyScanContLine
```

Of course, you need to replace `<beamline_repo>` with the name of your beamline repository.

Next, we will define the test for the scan. 

```python
def test_TutorialFlyScanContLine():
    # create a fake device manager that we can use to add devices
    device_manager = DMMock()  
    device_manager.add_device("samx")

    request = TutorialFlyScanContLine(
        motor="samx", start=0, stop=5, relative=False, device_manager=device_manager
    )
```

So far, the test has created a fake device manager and initialized the scan. We will now mock the `request_is_completed` method to simulate the device's response. 

```python
    with mock.patch.object(request.stubs, "request_is_completed", side_effect=[False, True]):
        reference_commands = list(request.run())
```

This test configuration will run two rounds within the while loop: On the first round, the `request_is_completed` method will return `False`, and on the second round, it will return `True`. All device instructions will be stored in the `reference_commands` list.

Finally, we will check if the scan worker receives the correct instructions. To ignore the request ID (`RID`) field, we will replace it with a fixed value.

```python
    for cmd in reference_commands:
        if not cmd:
            continue
        if "RID" in cmd.metadata:
            cmd.metadata["RID"] = "1948acad-afac-4f73-9492-2e10a084db91"

    assert reference_commands == [
        None,
        None,
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 0},
            device=None,
            action="open_scan",
            parameter={
                "scan_motors": [],
                "readout_priority": {
                    "monitored": [],
                    "baseline": [],
                    "on_request": [],
                    "async": [],
                },
                "num_points": None,
                "positions": [[0], [5]],
                "scan_name": "tutorial_cont_line_fly_scan",
                "scan_type": "fly",
            },
        ),
        ... # add the rest of the instructions here
    ]
```

````{dropdown} Full Test Code
```python
from unittest import mock

from bec_lib.messages import DeviceInstructionMessage
from bec_server.device_server.tests.utils import DMMock

from tomcat_bec.scans import TutorialFlyScanContLine


def test_TutorialFlyScanContLine():
    # create a fake device manager that we can use to add devices
    device_manager = DMMock()
    device_manager.add_device("samx")

    request = TutorialFlyScanContLine(
        motor="samx", start=0, stop=5, relative=False, device_manager=device_manager
    )

    with mock.patch.object(request.stubs, "request_is_completed", side_effect=[False, True]):
        reference_commands = list(request.run())

    for cmd in reference_commands:
        if not cmd:
            continue
        if "RID" in cmd.metadata:
            cmd.metadata["RID"] = "1948acad-afac-4f73-9492-2e10a084db91"

    assert reference_commands == [
        None,
        None,
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 0},
            device=None,
            action="open_scan",
            parameter={
                "scan_motors": [],
                "readout_priority": {
                    "monitored": [],
                    "baseline": [],
                    "on_request": [],
                    "async": [],
                },
                "num_points": None,
                "positions": [[0], [5]],
                "scan_name": "tutorial_cont_line_fly_scan",
                "scan_type": "fly",
            },
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 1},
            device=None,
            action="stage",
            parameter={},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "baseline", "DIID": 2},
            device=None,
            action="baseline_reading",
            parameter={},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 3},
            device=None,
            action="pre_scan",
            parameter={},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 4},
            device="samx",
            action="set",
            parameter={"value": 0, "wait_group": "scan_motor"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 5},
            device=["samx"],
            action="wait",
            parameter={"type": "move", "wait_group": "scan_motor"},
        ),
        DeviceInstructionMessage(
            metadata={
                "readout_priority": "monitored",
                "DIID": 6,
                "response": True,
                "RID": "1948acad-afac-4f73-9492-2e10a084db91",
            },
            device="samx",
            action="set",
            parameter={"value": 5, "wait_group": "set"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 7, "point_id": 0},
            device=None,
            action="trigger",
            parameter={"group": "trigger"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 8, "point_id": 0},
            device=None,
            action="read",
            parameter={"group": "primary", "wait_group": "readout_primary"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 9},
            device=None,
            action="wait",
            parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 10},
            device=None,
            action="wait",
            parameter={"type": "trigger", "time": 0, "group": "trigger"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 11, "point_id": 1},
            device=None,
            action="trigger",
            parameter={"group": "trigger"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 12, "point_id": 1},
            device=None,
            action="read",
            parameter={"group": "primary", "wait_group": "readout_primary"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 13},
            device=None,
            action="wait",
            parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 14},
            device=None,
            action="wait",
            parameter={"type": "trigger", "time": 0, "group": "trigger"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 15},
            device=None,
            action="wait",
            parameter={"type": "read", "group": "primary", "wait_group": "readout_primary"},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 16},
            device=None,
            action="complete",
            parameter={},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 17},
            device=None,
            action="unstage",
            parameter={},
        ),
        DeviceInstructionMessage(
            metadata={"readout_priority": "monitored", "DIID": 18},
            device=None,
            action="close_scan",
            parameter={},
        ),
    ]
```
````

<!-- ## Step 7: (Optional) Change client feedback from table to progress bar -->
