(developer.file_writer)=
## File Writer
BEC’s file writer is a dedicated service that writes HDF5 files with Nexus-compatible metadata entries to disk. It also adds external links to files written by other services, such as data backends for large 2D detector data. The internal structure of the files can be adjusted to the beamline’s needs using customizable plugins to comply with the desired [NeXus application definition](https://manual.nexusformat.org/classes/applications/index.html).

When the service starts, a `base_path` is configured, and all data can only be written to disk relative to this path. By default, the relative path follows the template `/data/S00000-S00999/S00001/S00001_master.h5` for scan number 1. To compile the appropriate path for secondary services, we provide the utility class [`bec_lib.file_utils.FileWriter`](/api_reference/_autosummary/bec_lib.file_utils.FileWriter.rst#bec_lib.file_utils.FileWriter) with the method [`compile_full_filename`](/api_reference/_autosummary/bec_lib.file_utils.FileWriter.rst#bec_lib.file_utils.FileWriter.compile_full_filename), which automatically prepares the correct filepath. 
If secondary services within *ophyd_devices* need to be configured with the appropriate file path, we recommend using this function since it will ensure that all custom changes to the file name and directory will be properly compiled and returned.

### Changing the File Directory or Adding a Suffix

The relative filepath can be configured and adapted dynamically. We use the metadata provided within BEC to inform the file writer about these changes. For this purpose, we reserve the keys `file_suffix` and `file_directory` in the metadata for scans. We note that both variables must only contain *alphanumeric ASCII* characters.
To configure these variables, we offer three different options:

1. **Handing the adjusted metadata directly to the scan command**: This method will only be considered for the given scan command but has the highest priority.
    ```python
    scans.line_scan(dev.samx, -5, 5, steps=100, relativ=True, metadata={'file_suffix': 'sampleA', 'file_directory': 'study1337'})
    ```

2. **Adding the information to `bec.metadata` in the command line interface**: This information will be considered for all following scans, unless explicitly overridden or deleted by a scan command.
    ```python
    bec.metadata.update({'file_suffix': 'sampleA', 'file_directory': 'study1337'})
    ```

3. **Using global variables [`bec.set_global_var`](/api_reference/_autosummary/bec_lib.client.BECClient.rst#bec_lib.client.BECClient.set_global_var)**: You can set `file_suffix` and `file_directory` as global variables within BEC, and they will be automatically considered. Note, this has the lowest priority compared to options 1 or 2.
