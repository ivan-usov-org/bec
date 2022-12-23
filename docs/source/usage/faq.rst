# 4. FAQ
## 4.1 Where should I implement a new scan?
The best place for implementing a new scan will depend on the specific circumstances. There are 4 locations with increasing complexity to implement a new scan:
   - Client: The client may be the most appropriate place if the scan is only used during one beamtime and is of little use to other experiments.
   - Scan server: Should the scan be reused frequently, adding it to the scan server also enables other clients to use the scan.
   - Device Server: For scans that only work with a specific hardware, it may be better to bundle the scan logic and the decice implementation in the device server. This can also be seen as a software-based fly scan.
   - Hardware controller: If the performance of software-based fly scans is insufficient (typically for acquisition rates >10 Hz), a hardware-based fly scan will likely be the best option.