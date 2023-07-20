How to create new scans
-----------------------

However, sometimes we want to run a sequence of functions as if it were a scan. For example, we might want to run a grid scan (2D scan) with our sample motor stages but move the sample position in z after each 2D scan. 
Normally, this would create multiple output files that one would need to merge together later. 

This is where the scan definition comes in: it allows us to run a sequence of functions as if it were a scan, resulting in a single :term:`scan_number`, a single :term:`scanID` and a single output file. 


.. code-block:: python

    @scans.scan_def
    def overnight_scan():
        open_shutter()
        samx_in()
        for i in range(10):
            scans.grid_scan(dev.samy, 0, 10, steps=100, exp_time=1, relative=False)
        samx_out()
        close_shutter()

By adding the decorator ``@scans.scan_def`` to the function definition, we mark this function as a scan definition.
