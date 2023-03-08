Quickstart
==========

Client
------------------------

    Please activate the proper environment as needed.

Device access
~~~~~~~~~~~~~~~~~

Devices are grouped in `dev`. This allows users to use tab-completion for finding devices.

.. image:: ../assets/tab-complete-devices.png
  :width: 300
  :alt: tab completion for finding devices
  :align: center

.. hint:: `dev` is imported as a builtin. As a result, you can access `dev` from everywhere. `dev` itself is just an alias for `bec.device_manager.devices`.

Inspect a device
~~~~~~~~~~~~~~~~~

.. code-block:: ipython

    LamNI [2/522] >> dev.samx

    Out[2]:
            Positioner(name=samx, enabled=True):
            --------------------
            Details:
                Status: enabled
                Last recorded value: {'value': 0, 'timestamp': 1671796007.547235}
                Device class: SynAxisOPAAS
                Acquisition group: motor
                Acquisition readoutPriority: monitored
                Device tags: ['user motors']
                User parameter: None
            --------------------
            Config:
                delay: 1
                labels: samx
                limits: [-50, 50]
                name: samx
                speed: 100
                tolerance: 0.01
                update_frequency: 400



Move a motor
~~~~~~~~~~~~~~

There are two variants of device movements: `updated move` and `move`.


Updated move (umv)
^^^^^^^^^^^^^^^^^^
A umv command blocks the command-line until the motor arrives at the target position (or an error occurs).

.. code-block:: python

    scans.umv(dev.samx, 5, relative=False)

Move (mv)
^^^^^^^^^^^^^^^^^^
A mv command is non-blocking, i.e. it does not wait until the motor reaches the target position. 

.. code-block:: python

    scans.mv(dev.samx, 5, relative=False)

However, it can be made a blocking call by 

.. code-block:: python

    scans.mv(dev.samx, 5, relative=False).wait()

The same mv command can also be executed by calling the device method `move`

.. code-block:: python

    dev.samx.move(5, relative=False)


.. note:: mv and umv can receive multiple devices, e.g. 

    .. code-block:: python
        
        scans.umv(dev.samx, 5, dev.samy, 10, relative=False)


Run a scan
~~~~~~~~~~~

All currently available scans are accessible through `scans.`, e.g.

.. code-block:: python

    s = scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1, relative=False)


.. 
    ### 3.2.3 Run a software based fly scan [TODO: MORE DETAILS]
    ```
    scans.round_scan_fly?
    scans.round_scan_fly(dev.flyer_sim, 0, 50, 5, 3, exp_time=0.1, relative=True)
    ```

Inspect the scan data
~~~~~~~~~~~~~~~~~~~~~~~~

The return value of a scan is a python object of type `ScanReport`. All data is stored in `<scan_report>.scan.data`, e.g.

.. code-block:: python

    s = scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1, relative=False)
    print(s.scan.data) # print the scan data

Load, save and update the configuration
----------------------------------------

Upload a new configuration
---------------------------

To upload a new device configuration from the client using a yaml file, please start all BEC services (if they are not running already) and run the following command from the client:

.. code-block:: python

    bec.config.update_session_with_file(<my-config.yaml>)

where :file:`<my-config.yaml>` is the full path to your device config file. 

Export the current configuration
---------------------------------

To save the current session to disk, use

.. code-block:: python

    bec.config.save_current_session("./config_saved.yaml") # this will save a file bec_client/config_saved.yaml


Update the configuration
-------------------------

Enable / disable a device
~~~~~~~~~~~~~~~~~~~~~~~~~~

To disable a device (e.g. samx), use

.. code-block:: python

    dev.samx.enabled=False # this disabled the device samx on all services and MongoDB

Update the device config
~~~~~~~~~~~~~~~~~~~~~~~~~~

To update the device config, use

.. code-block:: python

    dev.samx.set_device_config({"tolerance":0.02})

Set or update the user parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


To set the device's user parameters (such as in/out positions), use

.. code-block:: python

    dev.samx.set_user_parameter({"in": 2.6, "out": 0.2})

If instead you only want to update the user parameters, use

.. code-block:: python

    dev.samx.update_user_parameter({"in":2.8})


.. hint:: The user parameters can be seen as a python dictionary. Therefore, the above commands are equivalent to updating a python dictionary using 

    .. code-block:: python

        user_parameter = {"in": 2.6, "out": 0.2}    # equivalent to set_user_parameter
        print(f"Set user parameter: {user_parameter}")
        

        user_parameter.update({"in": 2.8})          # equivalent to update_user_parameter
        print(f"Updated user parameter: {user_parameter}")

    This will output:

    .. code-block:: 

        Set user parameter: {'in': 2.6, 'out': 0.2}
        Updated user parameter: {'in': 2.8, 'out': 0.2}

.. 
    ### 3.1.3 [TODO: TO BE DEVELOPED] Use **Web GUI tool** to update the configuration of current session in mongo database




