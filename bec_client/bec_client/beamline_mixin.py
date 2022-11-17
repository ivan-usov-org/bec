from rich import box, style
from rich.console import Console
from rich.table import Table


class BeamlineMixin:
    DEFAULT_STYLE = style.Style(color="green")
    ALARM_STYLE = style.Style(color="red", bold=True)

    def bl_show_all(self):
        pass

    @staticmethod
    def _get_info_val(info, entry):
        return str(info[entry]["value"])

    def sls_info(self):
        info = dev.sls_info.read(cached=True)
        console = Console()

        table = Table(title="SLS Info", box=box.SQUARE)
        table.add_column("Key", justify="center")
        table.add_column("Value", justify="center")

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

        table.add_row("Crane usage", self._get_info_val(info, "sls_info_crane_usage"))
        console.print(table)

    def _add_machine_status(self, table, info):
        val = self._get_info_val(info, "sls_info_operation")
        if val not in ["Light Available", "Light-Available"]:
            return table.add_row("Machine status", val, style=self.ALARM_STYLE)
        return table.add_row("Machine status", val, style=self.DEFAULT_STYLE)

    def _add_injection_mode(self, table, info):
        val = self._get_info_val(info, "sls_info_injection_mode")
        if val not in ["TOP-UP", "FREQ-REFILL"]:
            return table.add_row("Injection mode", val, style=self.ALARM_STYLE)
        return table.add_row("Injection mode", val, style=self.DEFAULT_STYLE)

    def _add_current_threshold(self, table, info):
        val = self._get_info_val(info, "sls_info_current_threshold")
        if val < 350:
            return table.add_row("Current threshold", val, style=self.ALARM_STYLE)
        return table.add_row("Current threshold", val, style=self.DEFAULT_STYLE)

    def _add_current_deadband(self, table, info):
        val = self._get_info_val(info, "sls_info_current_deadband")
        if val > 2:
            return table.add_row("Current deadband", val, style=self.ALARM_STYLE)
        return table.add_row("Current deadband", val, style=self.DEFAULT_STYLE)

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
        return table.add_row("SLS crane usage", f"{val:.2f} h", style=self.DEFAULT_STYLE)
