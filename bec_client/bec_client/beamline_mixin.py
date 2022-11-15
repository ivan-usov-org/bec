from rich.console import Console
from rich.table import Table
from rich import box


class BeamlineMixin:
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

        table.add_row("Operation", self._get_info_val(info, "sls_info_operation"), style="green")
        table.add_row("Injection mode", self._get_info_val(info, "sls_info_injection_mode"))
        table.add_row("Current threshold", self._get_info_val(info, "sls_info_current_threshold"))
        table.add_row("Current deadband", self._get_info_val(info, "sls_info_current_deadband"))
        table.add_row("SLS filling pattern", self._get_info_val(info, "sls_info_filling_pattern"))
        table.add_row(
            "SLS filling lifetime", self._get_info_val(info, "sls_info_filling_life_time")
        )
        table.add_row(
            "Orbit feedback mode", self._get_info_val(info, "sls_info_orbit_feedback_mode")
        )
        table.add_row(
            "Fast orbit feedback", self._get_info_val(info, "sls_info_fast_orbit_feedback")
        )
        table.add_row("Ring current", self._get_info_val(info, "sls_info_ring_current"))
        table.add_row("Machine status", self._get_info_val(info, "sls_info_machine_status"))
        table.add_row("Crane usage", self._get_info_val(info, "sls_info_crane_usage"))
        console.print(table)
        # print(capture.get())
        # 'sls_info_operation': {'value': 4, 'timestamp': 1668513745.471894},
        #  'sls_info_injection_mode': {'value': 0, 'timestamp': 1668509097.698679},
        #  'sls_info_current_threshold': {'value': 100.08,
        #   'timestamp': 1668513682.659547},
        #  'sls_info_current_deadband': {'value': 1.8, 'timestamp': 1668429763.942621},
        #  'sls_info_filling_pattern': {'value': 0, 'timestamp': 1668003328.055626},
        #  'sls_info_filling_life_time': {'value': 10.837996821263589,
        #   'timestamp': 1668514585.78606},
        #  'sls_info_orbit_feedback_mode': {'value': 1, 'timestamp': 1668513492.229837},
        #  'sls_info_fast_orbit_feedback': {'value': 0, 'timestamp': 1668513368.463382},
        #  'sls_info_ring_current': {'value': 102.04752098435712,
        #   'timestamp': 1668514586.193489},
        #  'sls_info_machine_status': {'value': 4, 'timestamp': 1668513745.471894},
        #  'sls_info_crane_usage': {'value': 0, 'timestamp': 1667911444.509}}
