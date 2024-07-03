
(developer.scans.scan_stubs)=
# Scan stubs - the building blocks of a scan
In order to simplify the creation of new scans, BEC provides a set of scan stubs that can be used as building blocks for new scans. The scan stubs are located in `bec_server/bec_server/scan_server/scan_stubs.py`. The following scan stubs are available:

*Device operations*
- [`set_and_wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.set_and_wait) Set a device to a value and wait for it to finish.
- [`read_and_wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.read_and_wait) Read a device and wait for it to finish.
- [`stage`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.stage) Stage a device.
- [`unstage`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.unstage) Unstage a device.
- [`kickoff`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.kickoff) Kickoff a device. Usually only needed for fly scans.
- [`complete`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.complete) Wait for a device to finish.
- [`get_req_status`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.get_req_status) Check if a device request status matches the given RID and DIID.
- [`get_device_progress`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.get_device_progress) Get the progress of a device. 
- [`pre_scan`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.pre_scan) Trigger the pre_scan method of a device.
- [`baseline_reading`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.baseline_reading) Trigger the baseline readings. 
- [`wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.wait) Wait for an event to finish. Could be a trigger, a readout or a movement. 
- [`read`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.read) Read from a device.
- [`trigger`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.trigger) Trigger a device.
- [`set`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.set) Set a device to a value.
- [`rpc`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.rpc) Send an RPC command to a device.
- [`send_rpc_and_wait`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.send_rpc_and_wait) Send an RPC command to a device and wait for it to finish.
- [`set_with_response`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.set_with_response) Set a device to a specific value and return the request ID. Use this method as an alternative to `kickoff` if the device does not support `kickoff`. 
- [`request_is_completed`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.request_is_completed) Check if a request that was initiated with `set_with_response` is completed.

*Scan operations*
- [`open_scan`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.open_scan) Open a scan.
- [`close_scan`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.close_scan) Close a scan. 
- [`publish_data_as_read`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.publish_data_as_read) Publish data as read.
- [`open_scan_def`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.open_scan_def) Open a scan definition. 
- [`close_scan_def`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.close_scan_def) Close a scan definition. 
- [`scan_report_instruction`](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs.scan_report_instruction) Update the scan report instruction.

More information on the scan stubs can be found in the [API reference](/api_reference/_autosummary/bec_server.scan_server.scan_stubs.ScanStubs.rst#bec_server.scan_server.scan_stubs.ScanStubs).
