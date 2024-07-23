(developer.event_data)=
# Event Data
Understanding the event system in BEC is crucial to benefit from the full capabilities of the system. BEC services are communicating with each other through messages on REDIS. A brief introduction to this concept is given in the previous section (TODO: link to previous section). 
Information is exchanged through various messages, which are published on specific endpoints in REDIS. 
Any service (of BEC) can be configured to act upon receiving updates on these endpoints. This is a powerful feature, as it allows you to react to any changes in the system and to trigger custom actions based on the events.
To give a more specific example, we can look at the preparation for a scan. The *ScanServer* will publish a [*ScanStatusMessage*](/api_reference/_autosummary/bec_lib.messages.ScanStatusMessage) which informs all other services about an upcoming scan. The *ScanStatusMessage* has also relevant information about the scan, which allows the *DeviceServer* to forward this information to all devices. In the end, each device can follow a customised sequence of actions to prepare itself for the upcoming scan based on the *ScanStatusMessage*.
In the following, we will show how to access commonly used event types in BEC and how to subscribe to them.

## Commonly used event types
To access the information of the endpoints, you have to be aware of the allowed message operations and the message types for the given endpoint. How to access this information is explained in the message introduction section (TODO: link to message introduction).
All message types inherit from the [`BECMessage`](/api_reference/_autosummary/bec_lib.messages.BECMessage) class, which ensures that a *content* and *metadata* field exists. Depending on the message type, the content and metadata can be different.
Below, we give a few examples of commonly used endpoints and how to access them from within the *BECIPythonClient*.

**Scan Status**
The [`scan_status`](/api_reference/_autosummary/bec_lib.endpoints.MessageEndpoints.scan_status) endpoint allows you to access information about the current/upcoming scan in BEC. We can check the status of the scan, the scan_ID, the scan_type, scan_args and scan_kwargs, as well as information about readoutPriority of devices, i.e. baseline, monitored, async etc. 
To access this information, we have to check first the message type and allowed operations for this endpoing.
``` ipython
[52/371] ❯❯ MessageEndpoints.scan_status().message_type
Out[52]: bec_lib.messages.ScanStatusMessage
[53/371] ❯❯ MessageEndpoints.scan_status().message_op
Out[53]: <MessageOp.SET_PUBLISH: ['register', 'set_and_publish', 'delete', 'get', 'keys']>
```
The message type is a [`ScanStatusMessage`](/api_reference/_autosummary/bec_lib.messages.ScanStatusMessage) and the allowed operations are `register`, `set_and_publish`, `delete`, `get` and `keys`. Please check the (TODO section) for more information on the allowed operations.

Let's assume we now want to access this information from the *BECIPythonClient*. We can use the following code:
```python
from bec_lib.endpoints import MessageEndpoints
msg = bec.connector.get(MessageEndpoints.scan_status())
msg.content # Content of the ScanStatusMessage
msg.metadata # Metadata of the ScanStatusMessage
```

**Scan Number**
The [`scan_number`](/api_reference/_autosummary/bec_lib.endpoints.MessageEndpoints.scan_number) endpoint allows you to access the current scan number. The message type is a [`VariableMessage`](/api_reference/_autosummary/bec_lib.messages.VariableMessage) and the allowed operations are `set`, `get`, `delete` and `keys`.
To access the current scan number, we can use the following code:
```python
from bec_lib.endpoints import MessageEndpoints
msg = bec.connector.get(MessageEndpoints.scan_number())
current_scan_number = msg.content["value"]
```

**Device Read and Read_Configuration**
The next two common endpoint that we would like to introduce are [`device_read`](/api_reference/_autosummary/bec_lib.endpoints.MessageEndpoints.device_read) and [`device_read_configuration`](/api_reference/_autosummary/bec_lib.endpoints.MessageEndpoints.device_read_configuration). These two endpoints give access to the last updated information of device signals of type *ophyd.Kind.normal/hinted* or *ophyd.Kind.config* respectively. In both cases, the message_type is a [`DeviceMessage`](/api_reference/_autosummary/bec_lib.messages.DeviceMessage) and the allowed operations are `register`, `set_and_publish`, `delete`, `get` and `keys`. 
To access for example the last *device_read* message, we can use the following code:

```python
from bec_lib.endpoints import MessageEndpoints
msg = bec.connector.get(MessageEndpoints.device_read())
msg.content # Content of the ScanStatusMessage
msg.metadata # Metadata of the ScanStatusMessage
```

```{note}
The *device_read* and *device_read_configuration* endpoints are updated whenever a device signal is updated. From the *BECIPythonClient*, forcing a device to update would be done by calling the `read(cached=False)` or `read_configuration(cached=False)` methods respectively.
```

**Scan Segment**
The [`scan_segment`](/api_reference/_autosummary/bec_lib.endpoints.MessageEndpoints.scan_segment) endpoint allows you to access the data of a scan segment, which corresponds to specific readings of devices with `readoutPriority = monitored`. Please check the device_configuration section for more information about the [readout_priority](developer.ophyd_device_config). 
In a step scan, the scan segment is updated after each step, while in a fly scan, the scan segment is updated based on the procedure defined by the scan. The message type is a [`ScanMessage`](/api_reference/_autosummary/bec_lib.messages.ScanMessage) and the allowed operations are `register`, `send`. As you see from the allowed operations, we can not directly get the last scan segment, but we can subscribe to the endpoint and receive the scan segments as they are published. We will show how to subscribe to an endpoint in the next section.

(developer.event_data.subscription)=
## Subscribing to events
Subscribing to events allows you to react to any new message published on a specific endpoint. We can do so by registering a callback function that will be executed whenever the endpoint publishes a new message. This all happens in the same thread, we therefore need to be careful with the execution time of the callback function.
The callback function will receive a [`bec_lib.connector.MessageObject`](/api_reference/_autosummary/bec_lib.connector.MessageObject) as input, with *topic* as a field for the endpointinfo in REDIS and *value* with the respective BECMessage. Therefore, we need to write our callback function to be capable of handling *ScanMessage*. Let's assume our scan has at least 21 points, we can then use the following callback to print a line once data for point 20 is published:
``` python
def my_cb(msg, **kwargs):
    if msg.value.content["point_id"] ==20:
        print("Point 20 is done")
        # My custom api call
```
After defining the callback function, we can subscribe to the endpoint with the following code:
```python
bec.connector.subscribe(MessageEndpoints.scan_segment(), my_cb)
```
Any new message published on the *scan_segment* endpoint will now trigger the callback function. 

```{note}
It is very important to keep the execution time of the callback function as short as possible. If the callback function takes too long to execute, it will block the thread and may compromise the performance of the system. For secondary operations, we recommend the callback function to trigger actions through an API call to a separate service.
```

## Accessing event data outside of the BECIPythonClient

If you like to use the event data oustide of the *BECIPythonClient*, you can use the [`RedisConnector`](/api_reference/_autosummary/bec_lib.redis_connector.RedisConnector) to access the REDIS server. You have to provide the correct `'host:port'` to the connector which allows you to connect to REDIS from the system you are running the code. If REDIS runs locally, this would be `'localhost:6379'`.
Note, at the beamline this would be the hostname of the bec_server. The port `6379` is the default port for REDIS. 
```python
from bec_lib.endpoints import MessageEndpoints
from bec_lib.redis_connector import RedisConnector
bootstrap = "localhost:6379" 
connector = RedisConnector(bootstrap)
connector.get(MessageEndpoints.device_read())
```

