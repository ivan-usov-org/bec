import abc
import typing

import h5py
import numpy as np
import xmltodict


class NeXusLayoutError(Exception):
    pass


class FileWriter(abc.ABC):
    def configure(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    def write(self, file_path: str, data):
        ...

    @staticmethod
    def _create_device_data_storage(data):
        device_storage = {}
        for point in range(data.num_points):
            for dev in data.scan_segments[point]:
                if dev not in device_storage:
                    device_storage[dev] = [data.scan_segments[point][dev][dev]["value"]]
                device_storage[dev].append(data.scan_segments[point][dev][dev]["value"])
        for dev_name, value in data.baseline.items():
            device_storage[dev_name] = value[dev_name]["value"]
        return device_storage


class XMLWriter:
    @staticmethod
    def get_type(type_string: str):
        if type_string == "float":
            return float
        if type_string == "string":
            return str
        if type_string == "int":
            return int
        raise NeXusLayoutError(f"Unsupported data type {type_string}.")

    def get_value(self, value, entry, source, data_type):
        if source == "constant":
            if data_type:
                return self.get_type(data_type)(value)
            return value
        return entry

    def add_group(self, container, val):
        name = val.pop("@name")
        group = container.create_group(name)
        self.add_content(group, val)

    def add_dataset(self, container, val):
        name = val.pop("@name")
        source = val.pop("@source")
        value = val.pop("@value", None)
        data_type = val.pop("@type", None)
        entry = val.pop("@entry", None)

        data = self.get_value(value=value, entry=entry, source=source, data_type=data_type)
        if data is None:
            return
        dataset = container.create_dataset(name, data=data)
        self.add_content(dataset, val)
        return

    def add_attribute(self, container, val):
        name = val.pop("@name")
        source = val.pop("@source")
        value = val.pop("@value", None)
        data_type = val.pop("@type", None)
        entry = val.pop("@entry", None)

        data = self.get_value(value=value, entry=entry, source=source, data_type=data_type)
        setattr(container.attrs, name, data)

    def add_hardlink(self, container, val):
        pass

    def add_softlink(self, container, val):
        pass

    def add_content(self, container, layout):
        for key, values in layout.items():
            if not isinstance(values, list):
                values = [values]
            for val in values:
                if key == "group":
                    self.add_group(container, val)
                elif key == "hdf5_layout":
                    self.add_base_entry(container, val)
                elif key == "attribute":
                    self.add_attribute(container, val)
                elif key == "dataset":
                    self.add_dataset(container, val)
                elif key == "hardlink":
                    self.add_hardlink(container, val)
                elif key == "softlink":
                    self.add_softlink(container, val)
                else:
                    pass
                    # raise NeXusLayoutError()

    def add_base_entry(self, container, val):
        self.add_group(container, val["group"])


class NeXusFileXMLWriter(FileWriter, XMLWriter):
    def configure(self, layout_file, **kwargs):
        self.layout_file = layout_file
        with open(self.layout_file, "br") as f:
            self.layout = xmltodict.parse(f)

    def get_value(self, value, entry, source, data_type):
        if source == "constant":
            if data_type:
                return self.get_type(data_type)(value)
            return value
        if source == "bec":
            return self.data.get(entry)
        return entry

    def write(self, file_path: str, data):
        print(f"writing file to {file_path}")
        self.data = self._create_device_data_storage(data)

        with h5py.File(file_path, "w") as file:
            self.add_content(file, self.layout)


class HDF5Storage:
    def __init__(self, storage_type: str = "group", data=None) -> None:
        self._storage = {}
        self._storage_type = storage_type
        self.attrs = {}
        self._data = data

    def create_group(self, name: str):
        self._storage[name] = HDF5Storage(storage_type="group")
        return self._storage[name]

    def create_dataset(self, name: str, data: typing.Any):
        self._storage[name] = HDF5Storage(storage_type="dataset", data=data)
        return self._storage[name]


class HDF5StorageWriter:
    device_storage = None

    def add_group(self, name: str, container: typing.Any, val: HDF5Storage):
        group = container.create_group(name)
        self.add_attribute(group, val.attrs)
        self.add_content(group, val._storage)

        if name == "bec" and container.attrs.get("NX_class") == "NXcollection":
            for key, value in self.device_storage.items():
                if value is None:
                    continue
                if isinstance(value, dict):

                    sub_storage = HDF5Storage(key)
                    dict_to_storage(sub_storage, value)
                    self.add_group(key, group, sub_storage)
                    # self.add_content(group, sub_storage._storage)
                    continue

                group.create_dataset(name=key, data=value)

    def add_dataset(self, name: str, container: typing.Any, val: HDF5Storage):
        data = val._data
        if data is None:
            return
        dataset = container.create_dataset(name, data=data)
        self.add_attribute(dataset, val.attrs)
        self.add_content(dataset, val._storage)
        return

    def add_attribute(self, container: typing.Any, attributes: dict):
        for name, value in attributes.items():
            if value is not None:
                container.attrs[name] = value

    def add_hardlink(self, container, val):
        pass

    def add_softlink(self, container, val):
        pass

    def add_content(self, container, storage):
        for name, val in storage.items():
            if val._storage_type == "group":
                self.add_group(name, container, val)
            elif val._storage_type == "dataset":
                self.add_dataset(name, container, val)
            elif val._storage_type == "hardlink":
                self.add_hardlink(container, val)
            elif val._storage_type == "softlink":
                self.add_softlink(container, val)
            else:
                pass

    @classmethod
    def write_to_file(cls, writer_storage, device_storage, file):
        writer = cls()
        writer.device_storage = device_storage
        writer.add_content(file, writer_storage)


class NexusFileWriter(FileWriter):
    def write(self, file_path: str, data):
        print(f"writing file to {file_path}")
        device_storage = self._create_device_data_storage(data)
        device_storage["metadata"] = data.metadata
        writer_storage = cSAXS_NeXus_format(HDF5Storage(), device_storage)

        with h5py.File(file_path, "w") as file:
            HDF5StorageWriter.write_to_file(writer_storage._storage, device_storage, file)


def dict_to_storage(storage, data):
    for key, val in data.items():
        if isinstance(val, dict):
            sub = storage.create_group(key)
            dict_to_storage(sub, val)
            continue
        storage.create_dataset(key, val)


def cSAXS_NeXus_format(storage, data):
    # /entry
    entry = storage.create_group("entry")
    entry.attrs["NX_class"] = "NXentry"
    entry.attrs["definition"] = "NXsas"
    entry.attrs["start_time"] = data.get("start_time")
    entry.attrs["version"] = 1.0

    # /entry/collection
    collection = entry.create_group("collection")
    collection.attrs["NX_class"] = "NXcollection"
    bec_collection = collection.create_group("bec")

    # /entry/control
    control = entry.create_group("control")
    control.attrs["NX_class"] = "NXmonitor"
    control.create_dataset(name="mode", data="monitor")
    control.create_dataset(name="integral", data=data.get("bpm4s"))

    # /entry/data

    # /entry/sample
    control = entry.create_group("sample")
    control.attrs["NX_class"] = "NXsample"
    control.create_dataset(name="name", data=data.get("samplename"))
    control.create_dataset(name="description", data=data.get("sample_description"))
    x_translation = control.create_dataset(name="x_translation", data=data.get("samx"))
    x_translation.attrs["units"] = "mm"
    y_translation = control.create_dataset(name="y_translation", data=data.get("samy"))
    y_translation.attrs["units"] = "mm"
    temperature_log = control.create_dataset(name="temperature_log", data=data.get("temp"))
    temperature_log.attrs["units"] = "K"

    # /entry/instrument
    instrument = entry.create_group("instrument")
    instrument.attrs["NX_class"] = "NXinstrument"
    instrument.create_dataset(name="name", data="cSAXS beamline")

    source = instrument.create_group("source")
    source.attrs["NX_class"] = "NXsource"
    source.create_dataset(name="type", data="Synchrotron X-ray Source")
    source.create_dataset(name="name", data="Swiss Light Source")
    source.create_dataset(name="probe", data="x-ray")
    distance = source.create_dataset(name="distance", data=-33800 - np.asarray(data.get("samz", 0)))
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
    source.create_dataset(name="type", data="undulator")
    gap = source.create_dataset(name="gap", data=data.get("idgap"))
    gap.attrs["units"] = "mm"
    k = source.create_dataset(name="k", data=2.46)
    k.attrs["units"] = "NX_DIMENSIONLESS"
    length = source.create_dataset(name="length", data=1820)
    length.attrs["units"] = "mm"

    slit_0 = instrument.create_group("slit_0")
    slit_0.attrs["NX_class"] = "NXslit"
    source.create_dataset(name="material", data="OFHC Cu")
    source.create_dataset(name="description", data="Horizontal secondary source slit")
    x_gap = source.create_dataset(name="x_gap", data=data.get("sl0wh"))
    x_gap.attrs["units"] = "mm"
    x_translation = source.create_dataset(name="x_translation", data=data.get("sl0ch"))
    x_translation.attrs["units"] = "mm"
    distance = source.create_dataset(name="distance", data=-21700 - np.asarray(data.get("samz", 0)))
    distance.attrs["units"] = "mm"

    slit_1 = instrument.create_group("slit_1")
    slit_1.attrs["NX_class"] = "NXslit"
    source.create_dataset(name="material", data="OFHC Cu")
    source.create_dataset(name="description", data="Horizontal secondary source slit")
    x_gap = source.create_dataset(name="x_gap", data=data.get("sl1wh"))
    x_gap.attrs["units"] = "mm"
    y_gap = source.create_dataset(name="y_gap", data=data.get("sl1wv"))
    y_gap.attrs["units"] = "mm"
    x_translation = source.create_dataset(name="x_translation", data=data.get("sl1ch"))
    x_translation.attrs["units"] = "mm"
    height = source.create_dataset(name="x_translation", data=data.get("sl1cv"))
    height.attrs["units"] = "mm"
    distance = source.create_dataset(name="distance", data=-7800 - np.asarray(data.get("samz", 0)))
    distance.attrs["units"] = "mm"

    mono = instrument.create_group("monochromator")
    mono.attrs["NX_class"] = "NXmonochromator"
    wavelength = mono.create_dataset(
        name="wavelength", data=12.3984193 / (data.get("mokev", -1) + 1e-9)
    )
    wavelength.attrs["units"] = "Angstrom"
    energy = mono.create_dataset(name="energy", data=data.get("mokev"))
    energy.attrs["units"] = "keV"
    mono.create_dataset(name="type", data="Double crystal fixed exit monochromator.")
    distance = mono.create_dataset(name="distance", data=-5220 - np.asarray(data.get("samz", 0)))
    distance.attrs["units"] = "mm"

    crystal_1 = mono.create_group("crystal_1")
    crystal_1.attrs["NX_class"] = "NXcrystal"
    crystal_1.create_dataset(name="usage", data="Bragg")
    crystal_1.create_dataset(name="order_no", data="1")
    crystal_1.create_dataset(name="reflection", data="[1 1 1]")
    bragg_angle = crystal_1.create_dataset(name="bragg_angle", data=data.get("moth1"))
    bragg_angle.attrs["units"] = "degrees"

    crystal_2 = mono.create_group("crystal_2")
    crystal_2.attrs["NX_class"] = "NXcrystal"
    crystal_2.create_dataset(name="usage", data="Bragg")
    crystal_2.create_dataset(name="order_no", data="2")
    crystal_2.create_dataset(name="reflection", data="[1 1 1]")
    bragg_angle = crystal_2.create_dataset(name="bragg_angle", data=data.get("moth1"))
    bragg_angle.attrs["units"] = "degrees"
    bend_x = crystal_2.create_dataset(name="bend_x", data=data.get("mobd"))
    bend_x.attrs["units"] = "degrees"

    xbpm4 = instrument.create_group("XBPM4")
    xbpm4.attrs["NX_class"] = "NXdetector"
    xbpm4_sum = xbpm4.create_group("XBPM4_sum")
    xbpm4_sum_data = xbpm4_sum.create_dataset(name="data", data=data.get("bpm4s"))
    xbpm4_sum_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm4_sum.create_dataset(name="description", data="Sum of counts for the four quadrants.")
    xbpm4_x = xbpm4.create_group("XBPM4_x")
    xbpm4_x_data = xbpm4_x.create_dataset(name="data", data=data.get("bpm4x"))
    xbpm4_x_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm4_x.create_dataset(
        name="description",
        data="Normalized difference of counts between left and right quadrants.",
    )
    xbpm4_y = xbpm4.create_group("XBPM4_y")
    xbpm4_y_data = xbpm4_y.create_dataset(name="data", data=data.get("bpm4y"))
    xbpm4_y_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm4_y.create_dataset(
        name="description",
        data="Normalized difference of counts between high and low quadrants.",
    )
    xbpm4_skew = xbpm4.create_group("XBPM4_skew")
    xbpm4_skew_data = xbpm4_skew.create_dataset(name="data", data=data.get("bpm4z"))
    xbpm4_skew_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm4_skew.create_dataset(
        name="description",
        data="Normalized difference of counts between diagonal quadrants.",
    )

    mirror = instrument.create_group("mirror")
    mirror.attrs["NX_class"] = "NXmirror"
    mirror.create_dataset(name="type", data="single")
    mirror.create_dataset(
        name="description",
        data="Grazing incidence mirror to reject high-harmonic wavelengths from the monochromator. There are three coating options available that are used depending on the X-ray energy, no coating (SiO2), rhodium (Rh) or platinum (Pt).",
    )
    incident_angle = mirror.create_dataset(name="incident_angle", data=data.get("mith"))
    incident_angle.attrs["units"] = "degrees"
    substrate_material = mirror.create_dataset(name="substrate_material", data="SiO2")
    substrate_material.attrs["units"] = "NX_CHAR"
    coating_material = mirror.create_dataset(name="coating_material", data="SiO2")
    coating_material.attrs["units"] = "NX_CHAR"
    bend_y = mirror.create_dataset(name="bend_y", data="mibd")
    bend_y.attrs["units"] = "NX_DIMENSIONLESS"
    distance = mirror.create_dataset(name="distance", data=-4370 - np.asarray(data.get("samz", 0)))
    distance.attrs["units"] = "mm"

    xbpm5 = instrument.create_group("XBPM5")
    xbpm5.attrs["NX_class"] = "NXdetector"
    xbpm5_sum = xbpm5.create_group("XBPM5_sum")
    xbpm5_sum_data = xbpm5_sum.create_dataset(name="data", data=data.get("bpm5s"))
    xbpm5_sum_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm5_sum.create_dataset(name="description", data="Sum of counts for the four quadrants.")
    xbpm5_x = xbpm5.create_group("XBPM5_x")
    xbpm5_x_data = xbpm5_x.create_dataset(name="data", data=data.get("bpm5x"))
    xbpm5_x_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm5_x.create_dataset(
        name="description",
        data="Normalized difference of counts between left and right quadrants.",
    )
    xbpm5_y = xbpm5.create_group("XBPM5_y")
    xbpm5_y_data = xbpm5_y.create_dataset(name="data", data=data.get("bpm5y"))
    xbpm5_y_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm5_y.create_dataset(
        name="description",
        data="Normalized difference of counts between high and low quadrants.",
    )
    xbpm5_skew = xbpm5.create_group("XBPM5_skew")
    xbpm5_skew_data = xbpm5_skew.create_dataset(name="data", data=data.get("bpm5z"))
    xbpm5_skew_data.attrs["units"] = "NX_DIMENSIONLESS"
    xbpm5_skew.create_dataset(
        name="description",
        data="Normalized difference of counts between diagonal quadrants.",
    )

    slit_2 = instrument.create_group("slit_2")
    slit_2.attrs["NX_class"] = "NXslit"
    source.create_dataset(name="material", data="Ag")
    source.create_dataset(name="description", data="Slit 2, optics hutch")
    x_gap = source.create_dataset(name="x_gap", data=data.get("sl2wh"))
    x_gap.attrs["units"] = "mm"
    y_gap = source.create_dataset(name="y_gap", data=data.get("sl2wv"))
    y_gap.attrs["units"] = "mm"
    x_translation = source.create_dataset(name="x_translation", data=data.get("sl2ch"))
    x_translation.attrs["units"] = "mm"
    height = source.create_dataset(name="x_translation", data=data.get("sl2cv"))
    height.attrs["units"] = "mm"
    distance = source.create_dataset(name="distance", data=-3140 - np.asarray(data.get("samz", 0)))
    distance.attrs["units"] = "mm"

    slit_3 = instrument.create_group("slit_3")
    slit_3.attrs["NX_class"] = "NXslit"
    source.create_dataset(name="material", data="Si")
    source.create_dataset(name="description", data="Slit 3, experimental hutch, exposure box")
    x_gap = source.create_dataset(name="x_gap", data=data.get("sl3wh"))
    x_gap.attrs["units"] = "mm"
    y_gap = source.create_dataset(name="y_gap", data=data.get("sl3wv"))
    y_gap.attrs["units"] = "mm"
    x_translation = source.create_dataset(name="x_translation", data=data.get("sl3ch"))
    x_translation.attrs["units"] = "mm"
    height = source.create_dataset(name="x_translation", data=data.get("sl3cv"))
    height.attrs["units"] = "mm"
    # distance = source.create_dataset(name="distance", data=-3140 - data.get("samz", 0))
    # distance.attrs["units"] = "mm"

    filter_set = instrument.create_group("filter_set")
    filter_set.attrs["NX_class"] = "NXattenuator"
    filter_set.create_dataset(name="material", data="Si")
    filter_set.create_dataset(
        name="description",
        data="The filter set consists of 4 linear stages, each with five filter positions. Additionally, each one allows for an out position to allow 'no filtering'.",
    )
    attenuator_transmission = filter_set.create_dataset(
        name="attenuator_transmission", data=10 ** data.get("ftrans", 0)
    )
    attenuator_transmission.attrs["units"] = "NX_DIMENSIONLESS"

    slit_4 = instrument.create_group("slit_4")
    slit_4.attrs["NX_class"] = "NXslit"
    source.create_dataset(name="material", data="Si")
    source.create_dataset(name="description", data="Slit 4, experimental hutch, exposure box")
    x_gap = source.create_dataset(name="x_gap", data=data.get("sl4wh"))
    x_gap.attrs["units"] = "mm"
    y_gap = source.create_dataset(name="y_gap", data=data.get("sl4wv"))
    y_gap.attrs["units"] = "mm"
    x_translation = source.create_dataset(name="x_translation", data=data.get("sl4ch"))
    x_translation.attrs["units"] = "mm"
    height = source.create_dataset(name="x_translation", data=data.get("sl4cv"))
    height.attrs["units"] = "mm"
    # distance = source.create_dataset(name="distance", data=-3140 - data.get("samz", 0))
    # distance.attrs["units"] = "mm"

    slit_5 = instrument.create_group("slit_5")
    slit_5.attrs["NX_class"] = "NXslit"
    source.create_dataset(name="material", data="Si")
    source.create_dataset(name="description", data="Slit 5, experimental hutch, exposure box")
    x_gap = source.create_dataset(name="x_gap", data=data.get("sl5wh"))
    x_gap.attrs["units"] = "mm"
    y_gap = source.create_dataset(name="y_gap", data=data.get("sl5wv"))
    y_gap.attrs["units"] = "mm"
    x_translation = source.create_dataset(name="x_translation", data=data.get("sl5ch"))
    x_translation.attrs["units"] = "mm"
    height = source.create_dataset(name="x_translation", data=data.get("sl5cv"))
    height.attrs["units"] = "mm"
    # distance = source.create_dataset(name="distance", data=-3140 - data.get("samz", 0))
    # distance.attrs["units"] = "mm"

    beam_stop_1 = instrument.create_group("beam_stop_1")
    beam_stop_1.attrs["NX_class"] = "NX_beamstop"
    beam_stop_1.create_dataset(name="description", data="circular")
    bms1_size = beam_stop_1.create_dataset(name="size", data=3)
    bms1_size.attrs["units"] = "mm"
    bms1_x = beam_stop_1.create_dataset(name="size", data=data.get("bs1x"))
    bms1_x.attrs["units"] = "mm"
    bms1_y = beam_stop_1.create_dataset(name="size", data=data.get("bs1y"))
    bms1_y.attrs["units"] = "mm"

    beam_stop_2 = instrument.create_group("beam_stop_2")
    beam_stop_2.attrs["NX_class"] = "NX_beamstop"
    beam_stop_2.create_dataset(name="description", data="rectangular")
    bms2_size_x = beam_stop_2.create_dataset(name="size_x", data=5)
    bms2_size_x.attrs["units"] = "mm"
    bms2_size_y = beam_stop_2.create_dataset(name="size_y", data=2.25)
    bms2_size_y.attrs["units"] = "mm"
    bms2_x = beam_stop_2.create_dataset(name="size", data=data.get("bs2x"))
    bms2_x.attrs["units"] = "mm"
    bms2_y = beam_stop_2.create_dataset(name="size", data=data.get("bs2y"))
    bms2_y.attrs["units"] = "mm"
    bms2_data = beam_stop_2.create_dataset(name="data", data=data.get("diode"))
    bms2_data.attrs["units"] = "NX_DIMENSIONLESS"

    return storage
