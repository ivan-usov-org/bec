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
            >>> scans.cont_line_fly_scan(dev.sam_rot, 0, 180, exp_time=0.1)

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
Next, we need to define the scan logic. In our case, the following steps are required:
- Move the motor to the start position.
- Send the flyer on its way to the defined stop position. 
- While the motor is moving, send triggers as fast as possible (respecting the exposure time).
- Stop the scan once the motor reaches the stop position.

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
            # read the data
            yield from self.stubs.read_and_wait(
                group="primary", wait_group="readout_primary", point_id=self.point_id
            )
            # wait for the trigger to complete
            yield from self.stubs.wait(
                wait_type="trigger", group="trigger", wait_time=self.exp_time
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
            >>> scans.cont_line_fly_scan(dev.sam_rot, 0, 180, exp_time=0.1)

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
            # read the data
            yield from self.stubs.read_and_wait(
                group="primary", wait_group="readout_primary", point_id=self.point_id
            )
            # wait for the trigger to complete
            yield from self.stubs.wait(
                wait_type="trigger", group="trigger", wait_time=self.exp_time
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