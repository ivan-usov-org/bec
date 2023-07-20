How to write a script
-----------------------

Scripts are user defined functions that can be executed from the BEC console. They are stored in the ``scripts`` folder and can be edited with any text editor. 
The scripts are loaded automatically on startup of the BEC console but can also be reloaded by typing ``bec.load_all_user_scripts()`` in the BEC console.
An example of a user script could be a function to move a specific motor to a predefined position:

.. code-block:: python 

    def samx_in():
        umv(dev.samx, 0)

or 

.. code-block:: python

    def close_shutter():
        print("Closing the shutter")
        umv(dev.shutter, 0)


A slightly more complex example could be a sequence of scans that are executed in a specific order:

.. code-block:: python

    def overnight_scan():
        open_shutter()
        samx_in()
        for i in range(10):
            scans.line_scan(dev.samy, 0, 10, steps=100, exp_time=1, relative=False)
        samx_out()
        close_shutter()

This script can be executed by typing ``overnight_scan()`` in the BEC console and would execute the following sequence of commands:

1. Open the shutter
2. Move the sample in
3. Perform 10 line scans on the sample
4. Move the sample out
5. Close the shutter