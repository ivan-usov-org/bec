(developer.scans)=
# BEC Scans
BEC uses scans to orchestrate the data acquisition. While script-based scans can also be defined in the command-line interface, acquisitions that require more complex orchestration should be defined as scan plugins for the BEC scan server. This section describes the basic structure of a scan and how to create a scan plugin.

## Scan Structure
A scan in BEC is a Python class that inherits from the `ScanBase` class and implements methods that should be executed in a specific order. The order of execution is defined by the `run` method, which is called by the scan server. By default, the `run` method calls the following methods in the following order:

```python
def run(self):
    """run the scan. This method is called by the scan server and is the main entry point for the scan."""
    self.initialize()
    yield from self.read_scan_motors()
    yield from self.prepare_positions()
    yield from self.scan_report_instructions()
    yield from self.open_scan()
    yield from self.stage()
    yield from self.run_baseline_reading()
    yield from self.pre_scan()
    yield from self.scan_core()
    yield from self.finalize()
    yield from self.unstage()
    yield from self.cleanup()
```

The `run` method is a generator function that like most other scan methods yields control to the scan server after each method call. This allows the scan server to handle asynchronous operations, such as moving motors or waiting for certain events. The scan server will call the next method in the scan after the current method has completed.

### Scan structure for a step scan
A step scan is a scan that acquires data at a series of positions, is generally the simplest type of scan and fully controlled by the scan server. 

#### Preparation for the scan
After reading out the current scan motor positions with `read_scan_motors`, the scan server will call the `prepare_positions` method to prepare the scan positions. Here, a relative position offset may be added depending on the user request (`relative=True` or `relative=False`).  

The `prepare_positions` method should yield an array of device positions with the shape `n x m` where `n` is the number of points in the scan and `m` is the number of scan motors. The scan server will then call the `open_scan` method to open the scan, followed by the `stage` method to stage the scan. The `scan_core` method is then called for each position in the list of positions. The `scan_core` method should yield the data to be saved for each position. After all positions have been scanned, the `finalize` method is called to finalize the scan. The `unstage` method is then called to unstage the scan, followed by the `cleanup` method to clean up any resources used by the scan.

#### Starting the scan


#### Scan core


#### Finalizing the scan and cleaning up


### Scan Structure for a Fly Scan