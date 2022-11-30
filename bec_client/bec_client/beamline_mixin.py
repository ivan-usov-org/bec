import builtins

from rich import box, style
from rich.console import Console
from rich.table import Table


class BeamlineMixin:
    DEFAULT_STYLE = style.Style(color="green")
    ALARM_STYLE = style.Style(color="red", bold=True)

    def bl_show_all(self):
        """Display general information about the SLS and the current status of the beamline"""
        self.beamline_info()
        self.sls_info()
        self.operator_messages()

    def beamline_info(self):
        """Display information about the current beamline status"""
        console = self._get_console()

        table = Table(title="X12SA Info", box=box.SQUARE)
        table.add_column("Key", justify="left")
        table.add_column("Value", justify="left")

        info = self._get_beamline_info_messages()
        self._add_op_status(table, info)
        self._add_id_gap(table, info)
        self._add_storage_ring_vac(table, info)
        self._add_shutter_status(table, info)
        self._add_mokev(table, info)
        self._add_fe_status(table, info)
        self._add_es1_valve(table, info)
        self._add_xbox1_pressure(table, info)
        self._add_xbox2_pressure(table, info)

        console.print(table)

    def _add_op_status(self, table, info):
        val = self._get_info_val(info, "x12sa_op_status")
        if val not in ["attended"]:
            return table.add_row("Beamline operation", val, style=self.ALARM_STYLE)
        return table.add_row("Beamline operation", val, style=self.DEFAULT_STYLE)

    def _add_shutter_status(self, table, info):
        val = self._get_info_val(info, "x12sa_es1_shutter_status")
        if val.lower() not in ["open"]:
            return table.add_row("Shutter", val, style=self.ALARM_STYLE)
        return table.add_row("Shutter", val, style=self.DEFAULT_STYLE)

    def _add_storage_ring_vac(self, table, info):
        val = self._get_info_val(info, "x12sa_storage_ring_vac")
        if val.lower() not in ["ok"]:
            return table.add_row("Storage ring vacuum", val, style=self.ALARM_STYLE)
        return table.add_row("Storage ring vacuum", val, style=self.DEFAULT_STYLE)

    def _add_es1_valve(self, table, info):
        val = self._get_info_val(info, "x12sa_es1_valve")
        if val.lower() not in ["open"]:
            return table.add_row("ES1 valve", val, style=self.ALARM_STYLE)
        return table.add_row("ES1 valve", val, style=self.DEFAULT_STYLE)

    def _add_xbox1_pressure(self, table, info):
        MAX_PRESSURE = 2e-6
        val = info["x12sa_exposure_box1_pressure"]["value"]
        if val > MAX_PRESSURE:
            return table.add_row(
                f"Exposure box 1 pressure (limit for opening the valve: {MAX_PRESSURE:.1e} mbar)",
                f"{val:.1e} mbar",
                style=self.ALARM_STYLE,
            )
        return table.add_row("Exposure box 1 pressure", f"{val:.1e} mbar", style=self.DEFAULT_STYLE)

    def _add_xbox2_pressure(self, table, info):
        MAX_PRESSURE = 2e-6
        val = info["x12sa_exposure_box2_pressure"]["value"]
        if val > MAX_PRESSURE:
            return table.add_row(
                f"Exposure box 2 pressure (limit for opening the valve: {MAX_PRESSURE:.1e} mbar)",
                f"{val:.1e} mbar",
                style=self.ALARM_STYLE,
            )
        return table.add_row("Exposure box 2 pressure", f"{val:.1e} mbar", style=self.DEFAULT_STYLE)

    def _add_fe_status(self, table, info):
        val = self._get_info_val(info, "x12sa_fe_status")
        return table.add_row("Front end shutter", val, style=self.DEFAULT_STYLE)

    def _add_id_gap(self, table, info):
        val = info["x12sa_id_gap"]["value"]
        if val > 8:
            return table.add_row("ID gap", f"{val:.3f} mm", style=self.ALARM_STYLE)
        return table.add_row("ID gap", f"{val:.3f} mm", style=self.DEFAULT_STYLE)

    def _add_mokev(self, table, info):
        val = info["x12sa_mokev"]["value"]
        return table.add_row("Selected energy (mokev)", f"{val:.3f} keV", style=self.DEFAULT_STYLE)

    def _get_beamline_info_messages(self) -> dict:
        dev = builtins.__dict__.get("dev")

        def _get_bl_msg(info, device_name):
            info[device_name] = dev[device_name].read(cached=True)

        info = {}
        _get_bl_msg(info, "x12sa_op_status")
        _get_bl_msg(info, "x12sa_storage_ring_vac")
        _get_bl_msg(info, "x12sa_es1_shutter_status")
        _get_bl_msg(info, "x12sa_id_gap")
        _get_bl_msg(info, "x12sa_mokev")
        _get_bl_msg(info, "x12sa_fe_status")
        _get_bl_msg(info, "x12sa_es1_valve")
        _get_bl_msg(info, "x12sa_exposure_box1_pressure")
        _get_bl_msg(info, "x12sa_exposure_box2_pressure")

        return info

    @staticmethod
    def _get_info_val(info, entry):
        return str(info[entry]["value"])

    def _get_operator_messages(self) -> dict:
        dev = builtins.__dict__.get("dev")
        info = dev.sls_operator.read(cached=True)
        if set(info.keys()) != {f"sls_operator_messages_message{i}" for i in range(1, 6)}:
            ValueError("Unexpected data structure for sls operator messages.")
        return info

    def _get_console(self) -> Console:
        return Console()

    def operator_messages(self):
        """Display information about the current SLS status"""

        console = self._get_console()
        table = Table(title="SLS Operator messages", box=box.SQUARE)
        table.add_column("Message", justify="left")
        table.add_column("Time", justify="left")

        info = self._get_operator_messages()

        for i in range(1, 6):
            msg = info[f"sls_operator_messages_message{i}"]["value"]
            date = info[f"sls_operator_date_message{i}"]["value"]
            if msg:
                table.add_row(msg, date)
        if table.row_count == 0:
            table.add_row("No messages available", "")
        console.print(table)

    def _get_sls_info(self) -> dict:
        dev = builtins.__dict__.get("dev")
        info = dev.sls_info.read(cached=True)
        return info

    def sls_info(self):
        """Display information about the current SLS status"""

        console = self._get_console()

        table = Table(title="SLS Info", box=box.SQUARE)
        table.add_column("Key", justify="left")
        table.add_column("Value", justify="left")

        info = self._get_sls_info()

        self._add_machine_status(table, info)
        self._add_injection_mode(table, info)
        self._add_ring_current(table, info)
        self._add_current_threshold(table, info)
        self._add_current_deadband(table, info)
        self._add_filling_pattern(table, info)
        self._add_filling_lifetime(table, info)
        self._add_ofb_mode(table, info)
        self._add_fofb(table, info)
        self._add_crane_usage(table, info)
        console.print(table)

    def _add_machine_status(self, table, info):
        val = self._get_info_val(info, "sls_info_machine_status")
        if val not in ["Light Available", "Light-Available"]:
            return table.add_row("Machine status", val, style=self.ALARM_STYLE)
        return table.add_row("Machine status", val, style=self.DEFAULT_STYLE)

    def _add_injection_mode(self, table, info):
        val = self._get_info_val(info, "sls_info_injection_mode")
        if val not in ["TOP-UP", "FREQ-REFILL"]:
            return table.add_row("Injection mode", val, style=self.ALARM_STYLE)
        return table.add_row("Injection mode", val, style=self.DEFAULT_STYLE)

    def _add_current_threshold(self, table, info):
        val = info["sls_info_current_threshold"]["value"]
        if val < 350:
            return table.add_row("Current threshold", str(val), style=self.ALARM_STYLE)
        return table.add_row("Current threshold", str(val), style=self.DEFAULT_STYLE)

    def _add_current_deadband(self, table, info):
        val = info["sls_info_current_deadband"]["value"]
        if val > 2:
            return table.add_row("Current deadband", str(val), style=self.ALARM_STYLE)
        return table.add_row("Current deadband", str(val), style=self.DEFAULT_STYLE)

    def _add_filling_pattern(self, table, info):
        val = self._get_info_val(info, "sls_info_filling_pattern")
        return table.add_row("Filling pattern", val, style=self.DEFAULT_STYLE)

    def _add_filling_lifetime(self, table, info):
        val = info["sls_info_filling_life_time"]["value"]
        return table.add_row("SLS filling lifetime", f"{val:.2f} h", style=self.DEFAULT_STYLE)

    def _add_ofb_mode(self, table, info):
        val = self._get_info_val(info, "sls_info_orbit_feedback_mode")
        if val not in ["fast"]:
            return table.add_row("Orbit feedback mode", val, style=self.ALARM_STYLE)
        return table.add_row("Orbit feedback mode", val, style=self.DEFAULT_STYLE)

    def _add_fofb(self, table, info):
        val = self._get_info_val(info, "sls_info_fast_orbit_feedback")
        if val not in ["running"]:
            return table.add_row("Fast orbit feedback", val, style=self.ALARM_STYLE)
        return table.add_row("Fast orbit feedback", val, style=self.DEFAULT_STYLE)

    def _add_ring_current(self, table, info):
        val = info["sls_info_ring_current"]["value"]
        if val < 300:
            return table.add_row("Ring current", f"{val:.3f} mA", style=self.ALARM_STYLE)
        return table.add_row("Ring current", f"{val:.3f} mA", style=self.DEFAULT_STYLE)

    def _add_crane_usage(self, table, info):
        val = self._get_info_val(info, "sls_info_crane_usage")
        return table.add_row("SLS crane usage", val, style=self.DEFAULT_STYLE)
