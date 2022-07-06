import abc

import h5py
import xmltodict


class FileWriter(abc.ABC):
    def configure(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def write(self, file_path: str, data):
        ...

    @staticmethod
    def _create_device_data_storage(data):
        device_storage = dict()
        for point in range(data.num_points):
            for dev in data.scan_segments[point]:
                if dev not in device_storage:
                    device_storage[dev] = [data.scan_segments[point][dev][dev]["value"]]
                device_storage[dev].append(data.scan_segments[point][dev][dev]["value"])
        return device_storage


class NeXusFileXMLWriter(FileWriter):
    def configure(self, layout_file, **kwargs):
        self.layout_file = layout_file
        with open(self.layout_file, "r") as f:
            self.layout = xmltodict.parse(f)

    def write(self, file_path: str, data):
        print(f"writing file to {file_path}")
        device_storage = self._create_device_data_storage(data)

        with h5py.File(file_path, "w") as file:
            entry = file.create_group("entry")
            entry.attrs["NX_class"] = "NXentry"
            entry.create_dataset("definition", "NXsas")
            instrument = entry.create_group("instrument")
            for dev in device_storage:
                instrument.create_dataset(name=dev, data=device_storage[dev])


class NexuFileWriter(FileWriter):
    def write(self, file_path: str, data):
        print(f"writing file to {file_path}")
        device_storage = self._create_device_data_storage(data)

        with h5py.File(file_path, "w") as file:

            # /entry
            entry = file.create_group("entry")
            entry.attrs["NX_class"] = "NXentry"

            # /entry/collection
            collection = entry.create_group("collection")
            collection.attrs["NX_class"] = "NXcollection"
            bec_collection = entry.create_group("bec")

            # /entry/control
            control = entry.create_group("control")
            control.attrs["NX_class"] = "NXmonitor"
            mode = control.create_dataset(name="mode", data="monitor")
            integral = control.create_dataset(name="integral", data=data["bpm4s"])

            # /entry/data

            # /entry/sample

            # /entry/instrument
            instrument = entry.create_group("instrument")
            instrument.attrs["NX_class"] = "NXinstrument"
            instrument.create_dataset(name="name", data="cSAXS beamline")

            source = instrument.create_group("source")
            source.attrs["NX_class"] = "NXsource"
            source.create_dataset(name="type", data="Synchrotron X-ray Source")
            source.create_dataset(name="name", data="Swiss Light Source")
            source.create_dataset(name="probe", data="x-ray")
            distance = source.create_dataset(name="distance", data=-33800 - data.get("samz", 0))
            distance.attrs["units"] = "mm"
            sigma_x = source.create_dataset(name="sigma_x", data=0.202)
            sigma_x.attrs["units"] = "mm"
            sigma_y = source.create_dataset(name="sigma_y", data=0.018)
            sigma_y.attrs["units"] = "mm"
            divergence_x = source.create_dataset(name="divergence_x", data=0.000135)
            divergence_x.attrs["units"] = "radians"
            divergence_y = source.create_dataset(name="divergence_y", data=0.000025)
            divergence_y.attrs["units"] = "radians"
            current = source.create_dataset(name="current", data=data.get("curr"))
            current.attrs["units"] = "mA"

            insertion_device = instrument.create_group("insertion_device")
            insertion_device.attrs["NX_class"] = "NXinsertion_device"
