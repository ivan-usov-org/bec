import abc

import h5py


class FileWriter(abc.ABC):
    def configure(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def write(self, file_path: str, data):
        ...


class NeXusFileWriter(FileWriter):
    def write(self, file_path: str, data):
        file = h5py.File(file_path, "w")
        entry = file.create_group("entry")
        entry.attrs["NX_class"] = "NXentry"
        entry.create_dataset("definition", "NXsas")
        instrument = entry.create_group("instrument")

        device_storage = dict()
        for point in range(data.num_points):
            for dev in data.scan_segments[point]:
                if dev not in device_storage:
                    device_storage[dev] = [data.scan_segments[point][dev][dev]["value"]]
                device_storage[dev].append(data.scan_segments[point][dev][dev]["value"])
        for dev in device_storage:
            instrument.create_dataset(name=dev, data=device_storage[dev])
        file.close()
        print(f"writing file to {file_path}")
