import time
from rich.console import Console
from rich.table import Table
from rich import box


class LamNIOpticsMixin:
    def leyey_out(self):
        loptics_in()
        fshon()
        umv(dev.leyey, 0.5)

        # TODO filter

        epics_put("XOMNYI-XEYE-ACQ:0", 2)
        # umv dttrz 5236.1953 fttrz -2934.5479

    def leye_in(self):
        bec.queue.next_dataset_number += 1
        # umv dttrz 5236+600 fttrz -2934+600
        while True:
            moved_out = (input("Did the flight tube move out? (Y/n)") or "y").lower()
            if moved_out == "y":
                break
            if moved_out == "n":
                return
        umv(dev.leyex, 14.094, dev.leyey, 47.294)
        self.align.update_frame()

    def _lfzp_in(self):
        # umv loptx -0.549000 lopty 3.680000 #for 13 keV and 100 mu, 60 nm fzp
        pass

    def lfzp_in(self):
        if "rtx" in dev and dev.rtx.enabled:
            dev.rtx.feedback_disable()

        self._lfzp_in()

        if "rtx" in dev and dev.rtx.enabled:
            dev.rtx.feedback_enable_with_reset()

    def loptics_in(self):
        self.lfzp_in()
        self.losa_in()

    def _loptics_out(self):
        if "rtx" in dev and dev.rtx.enabled:
            dev.rtx.feedback_disable()

        self.lcs_out()
        self.losa_out()
        # umv loptx -0.549000-0.15 lopty 3.680000-0.15

        if "rtx" in dev and dev.rtx.enabled:
            time.sleep(1)
            dev.rtx.feedback_enable_with_reset()

    def lcs_in(self):
        # umv lcsx -1.852 lcsy -0.095
        pass

    def lcs_out(self):
        umv(dev.lcsy, 3)

    def losa_in(self):
        # 11 kev
        # umv(dev.losax, -1.1900, dev.losay, -0.1860)
        # umv(dev.losaz, 1.0)
        pass

    def losa_out(self):
        # umv losaz -3
        # umv losay 3.8
        pass

    def lfzp_info(self):
        loptz_val = dev.loptz.read()["loptz"]["value"]
        distance = -loptz_val + 85.6 + 52
        print(f"The sample is in a distance of {distance:.1f} mm from the FZP.")

        diameters = []
        diameters[0] = 80e-6
        diameters[1] = 100e-6
        diameters[2] = 120e-6
        diameters[3] = 150e-6
        diameters[4] = 170e-6
        diameters[5] = 200e-6
        diameters[6] = 220e-6
        diameters[7] = 250e-6

        mokev_val = dev.mokev.read()["mokev"]["value"]
        console = Console()
        table = Table(
            title=f"At the current energy of {mokev_val:.4f} keV we have following options:",
            box=box.SQUARE,
        )
        table.add_column("Diameter", justify="center")
        table.add_column("Focal distance", justify="center")
        table.add_column("Current beam size", justify="center")

        wavelength = 1.2398e-9 / mokev_val

        for diameter in diameters:
            outermost_zonewidth = 60e-9
            focal_distance = diameter * outermost_zonewidth / wavelength
            beam_size = (
                -diameter / (focal_distance * 1000) * (focal_distance * 1000 - distance) * 1e6
            )
            table.add_row(f"{diameter}", f"{focal_distance:.2f} mm", f"{beam_size:.2f} microns")

        console.print(table)

        print("OSA Information:")
        # print(f"Current losaz %.1f\n", A[losaz])
        # print("The OSA will collide with the sample plane at %.1f\n\n", 89.3-A[loptz])
        print(
            "The numbers presented here are for a sample in the plane of the lamni sample holder.\n"
        )
