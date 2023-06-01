import builtins
import time

bec = builtins.__dict__.get("bec")
dev = builtins.__dict__.get("dev")
umv = builtins.__dict__.get("umv")


class XTreme:
    def set_au_mesh(self, val: float):
        """Set the position of gold mesh, used for IO

        Args:
            val (float): target position for gold mesh

        Example:
            >>> xt.set_au_mesh(163.0)
        """
        umv(dev.goldmesh1, val)

    def set_slit(self, val: float):
        """Set the exit slit

        Args:
            val (float): width of the exit slit

        Example:
            >>> xt.set_slit(30)
        """
        umv(dev.exit_slit, val)

    def set_har(self, val: float):
        """Set the ID harmonics

        Args:
            val (float): Target value

        Example:
            >>> xt.set_har(1.0)
        """
        dev.harmonic.set(val).wait()

    def set_energy(self, val: float):
        """Set the x-ray energy. Internally, it will adjust the id gap and the mono accordingly.

        Args:
            val (float): Target energy in eV

        Example:
            >>> xt.set_energy(700.0)
        """
        dev.mono.with_undulator.set(1).wait()
        umv(dev.mono, val)


    def open_valve(self, delay=0.85):
        """Open the valve"""
        dev.valve.set(1).wait()
        time.sleep(delay)
        while True:
            valve_val = dev.valve.read()["valve"]["value"]
            if valve_val == 5:
                break
            print(f"Valve did not open. Current status: {valve_val}. Trying again...")
            time.sleep(1)
        print("Valve opened")

    def close_valve(self, delay=0.85):
        """Close the valve"""
        dev.valve.set(0).wait()
        time.sleep(delay)
        while True:
            valve_val = dev.valve.read()["valve"]["value"]
            if valve_val == 2:
                break
            print(f"Valve did not close. Current status: {valve_val}. Trying again...")
            time.sleep(1)
        print("Valve closed")

    def set_hor(self, val: float):
        """Set the horizontal position the endstation.

        Args:
            val (float): Target value

        Example:
            >>> xt.set_hor(104.5)
        """
        umv(dev.sample_hor, val)

    def set_rot(self, val: float):
        """Set the sample angle.

        Args:
            val (float): Target value

        Example:
            >>> xt.set_rot(60)
        """
        umv(dev.sample_rot, val)        

    def set_vert(self, val: float):
        """Set the vertical position the sample stick.

        Args:
            val (float): Target value

        Example:
            >>> xt.set_vert(7.5)
        """
        umv(dev.sample_vert, val)

    def set_hx(self, val: float):
        """Set the magnetic field (hx)

        Args:
            val (float): Target value.

        Example:
            >>> xt.set_hx(104.5)
        """
        umv(dev.field_x, val)

    def set_temp(self, val: float):
        """Set the sample temperature.

        Args:
            val (float): Target value.

        Example:
            >>> xt.set_temp(300.0)
        """
        umv(dev.temperature, val)

    def rampdown(self):
        """Set field_x and field_z to 0"""
        umv(dev.field_x, 0, dev.field_z, 0)

    def set_fe(self, opening: float):
        """Set the FE aperture. Must be either 0, 0.1, 0.25, 0.5, 1, 1.25 or 2.

        Args:
            opening (float): Opening value in mm.

        Example:
            >>> xt.set_fe(1)
        """
        # aperture returns an int, not a string?
        openings = [0, 0.1, 0.25, 0.5, 1, 1.25, 2]
        if opening not in openings:
            raise ValueError(f"FE opening must be one of the following values: {openings}")

        if opening == 0:
            dev.aperture.set(0).wait()
        elif opening == 0.1:
            dev.aperture.set(1).wait()
        elif opening == 0.25:
            dev.aperture.set(2).wait()            
        elif opening == 0.5:
            dev.aperture.set(3).wait()            
        elif opening == 1:
            dev.aperture.set(4).wait()            
        elif opening == 1.25:
            dev.aperture.set(5).wait()                                    
        elif opening == 2:
            dev.aperture.set(6).wait()                                    

    def wait_temp(self):
        """Check if the 1K pot is refilling and wait if needed."""

        # # Not entirely sure what the script is supposed to do...
        # raise NotImplementedError()
        tcontrol = dev.tcontrol.read()
        tcontrol_on = tcontrol["tcontrol_control"]["value"]


        if not tcontrol_on:
            temp = dev.temperature.read()
            print(f"T auto control is not running. Setpoint = {temp['temperature']['value']} K.")
            return

        while True:
            tcontrol = dev.tcontrol.read()
            tstatus = tcontrol["tcontrol_status"]["value"]
            if tstatus == "Stable":
                print("T is now stable.")
                break
            tcontrol_on = tcontrol["tcontrol_control"]["value"]
            if not tcontrol_on:
                print("Tcontrol was switched off. Exiting.")
                break
            time.sleep(1)
        
    def set_keithley_range(self, keithley_index:int, gain:int):
        """Set the keithley range.

        Args:
            keithley_index (int): Keithley index, must be either 1, 2 or 3.
            gain (int): Keithley gain, must be in range 3-11. A value of 3 will set the gain to 10^3.

        Example:
            >>> xt.set_keithley_range(1, 9)
        """
        if keithley_index not in [1, 2, 3]:
            raise ValueError("Keithley index must be either 1, 2 or 3.")
        
        gains = list(range(3, 12))

        if gain not in gains:
            raise ValueError("Keithley gain must in range 3-11.")
        
        if gain < 11:
            dev[f"keithley_{keithley_index}"].set(gain-3)
        else:
            raise NotImplementedError()

        
