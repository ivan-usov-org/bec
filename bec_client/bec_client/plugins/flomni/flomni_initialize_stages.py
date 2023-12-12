

import time

import numpy as np


class FlomniInitError(Exception):
    pass

class FlomniError(Exception):
    pass

class FlomniInitStagesMixin:

    def flomni_init_stages(self):
        self.drive_axis_to_limit(dev.ftransy, "forward")
        dev.ftransy.limits = [-100, 0]

        self.drive_axis_to_limit(dev.ftransz, "reverse")
        dev.ftransz.limits = [0, 145]

        self.drive_axis_to_limit(dev.ftransx, "reverse")
        dev.ftransx.limits = [0, 50]

        self.drive_axis_to_limit(dev.feyey, "forward")
        dev.feyey.limits = [-1, -10]

        self.drive_axis_to_limit(dev.feyex, "forward")
        dev.feyex.limits = [-30, -1]

        user_input = input("Init of foptz. Can the stage move to the upstream limit without collision? [y/n]")
        if user_input == "y":
            print("good then")
        else:
            return
        
        self.drive_axis_to_limit(dev.foptz, "reverse")
        dev.foptz.limits = [0, 27]


        ## smaract stages
        max_repeat = 100
        repeat = 0
        axis_id_fosaz = dev.fosaz._config["deviceConfig"].get("axis_Id")
        axis_id_numeric_fosaz = self.axis_id_to_numeric(axis_id_fosaz)
        while True:
            curtain_is_triggered = dev.foptz.controller.fosaz_light_curtain_is_triggered()
            if curtain_is_triggered:
                break
            if repeat > max_repeat:
                raise FlomniInitError("Failed to initialize fosaz within 100 repeats.")
            dev.fosaz.controller.move_open_loop_steps(axis_id_numeric_fosaz, -500, amplitude=4000, frequency = 2000)
            time.sleep(1)
            repeat += 1
            

        for ii in range(3):
            dev.fosax.controller.find_reference_mark(ii, 0, 1000, 1)
            time.sleep(1)
        
        dev.fosax.limits = [10.2, 10.6]
        dev.fosay.limits = [-3.1, -2.9]
        dev.fosaz.limits = [-6, -4]
        # dev.fosax.controller.describe()

        umv(dev.fosaz, -5)
        umv(dev.fosax, 10.4, dev.fosay, -3)

        self.drive_axis_to_limit(dev.fcapy, "reverse")
        dev.fcapy.limits = [-15, 0]

        self.drive_axis_to_limit(dev.fsamy, "reverse")
        dev.fsamy.limits = [2, 3.1]

        user_input = input("Init of tracking stages. Did you remove the outer laser flight tubes? [y/n]")
        if user_input == "y":
            print("good then")
        else:
            print("Stopping.")
            return
        
        self.drive_axis_to_limit(dev.ftracky, "reverse")
        dev.ftracky.limits = [2.2, 2.8]

        self.drive_axis_to_limit(dev.ftrackz, "reverse")
        dev.ftrackz.limits = [4.5, 5.5]

        user_input = input("Init of sample stage. Is the piezo at about 0 deg? [y/n]")
        if user_input == "y":
            print("good then")
        else:
            print("Stopping.")
            return
        
        self.drive_axis_to_limit(dev.fsamx, "forward")
        dev.fsamx.limits = [-162, 0]

        self.drive_axis_to_limit(dev.ftray, "reverse")
        dev.ftray.limits = [-200, 0]

        print("Initializing UPR stage.")
        user_input = input("To ensure that the end switches work, please check that they are currently not pushed. Is everything okay? [y/n]")
        if user_input == "y":
            print("good then")
        else:
            print("Stopping.")
            return
        
        while True:
            low_limit, high_limit = dev.fsamroy.controller.get_motor_limit_switch("A")
            if not high_limit:
                print("Please push limit switch to the left.")
                time.sleep(1)
                continue
            break
        
        while True:
            low_limit, high_limit = dev.fsamroy.controller.get_motor_limit_switch("A")
            if not low_limit:
                print("Please push limit switch to the right.")
                time.sleep(1)
                continue
            break
        user_input = input("Shall I start the index search? [y/n]")
        if user_input == "y":
            print("good then")
        else:
            print("Stopping.")
            return
        if dev.fsamroy.controller.is_motor_on("A"):
            raise FlomniInitError("fsamroy should be off. Something is wrong. Mirko... help!")
        dev.fsamroy.controller.socket_put_confirmed("XQ#MOTON")
        dev.fsamroy.enabled = False
        time.sleep(5)
        dev.fsamroy.enabled = True
        time.sleep(2)
        dev.fsamroy.controller.socket_put_confirmed("XQ#REFAX")
        while not dev.fsamroy.controller.all_axes_referenced():
            print("Waiting for fsamroy to be referenced.")
            time.sleep(1)
        dev.fsamroy.limits = [-5, 365]

        user_input = input("Init of foptx. Can the stage move to the positive limit without collision? Attention: tracker flight tube! [y/n]")
        if user_input == "y":
            print("good then")
        else:
            print("Stopping.")
            return
        
        self.drive_axis_to_limit(dev.foptx, "forward")
        dev.foptx.limits = [-16, -14]

        axis_id_fopty = dev.fopty._config["deviceConfig"].get("axis_Id")
        
        while True:
            low_limit, high_limit = dev.fopty.controller.get_motor_limit_switch(axis_id_fopty)
            if not low_limit:
                print("To ensure that the fopty end switch works, please push it down and hold it for about 1 second.")
                time.sleep(1)
                continue
            break

        self.drive_axis_to_limit(dev.fopty, "reverse")
        dev.fopty.limits = [0, 4]

        self.set_limits()

    def set_limits(self):
        dev.ftransy.limits = [-100, 0]
        dev.ftransz.limits = [0, 145]
        dev.ftransx.limits = [0, 50]
        dev.ftray.limits = [-200, 0]
        dev.fsamy.limits = [2, 3.5]
        dev.foptz.limits = [22.5, 28]
        dev.foptx.limits = [-17, -12]
        dev.fcapy.limits = [-15, 0]
        dev.feyex.limits = [-18, -1]
        dev.feyey.limits = [-12, -1]
        dev.fopty.limits = [0, 4]
        dev.fosax.limits = [7, 10]
        dev.fosay.limits = [-4.2, 7]
        dev.fosaz.limits = [-6.5, 7.5]
        # dev.rtx.limits = [-220, 220]
        # dev.rty.limits = [-180, 180]
        # dev.rtz.limits = [-220, 220]
        dev.fsamroy.limits = [-5, 365]
        dev.ftracky.limits = [2.2, 2.8]
        dev.ftrackz.limits = [4.5, 5.5]

    def align_setup(self):

        # positions for optics out and 50 mm distance to sample
        umv(dev.ftrackz, 4.73, dev.ftracky, 2.5170, dev.foptx, -14.3, dev.fopty, 3.87)

        # the fopty 3.87 should put us in place for a lower FZP on the lower FZP chip

        umv(dev.foptz, 23)

        flomni_samx_in = dev.fsamx.user_parameter.get("in")
        if flomni_samx_in is None:
            raise FlomniInitError("Could not find a fsamx in position. Please check your device config.")
        umv(dev.fsamx, flomni_samx_in)
        flomni_samy_in = dev.fsamy.user_parameter.get("in")
        if flomni_samy_in is None:
            raise FlomniInitError("Could not find a fsamy in position. Please check your device config.")
        umv(dev.fsamy, flomni_samy_in)

        # after init reduce vertical stage speed
        dev.fsamy.controller.socket_put_confirmed("axspeed[5]=20000")

        umv(dev.feyey, -8)


class FlomniSampleTransferMixin:

    def ensure_osa_back(self):
        dev.fosaz.limits = [-12.6, -12.4]
        umv(dev.fosaz, -12.5)

        curtain_is_triggered = dev.fcapy.controller.fosaz_light_curtain_is_triggered()
        if not curtain_is_triggered:
            raise FlomniError("Fosaz did not reach light curtain")

    def ensure_fcapy_up(self):
        axis_id = dev.fcapy._config["deviceConfig"].get("axis_Id")
        axis_id_numeric = self.axis_id_to_numeric(axis_id)
        low, high = dev.fcapy.controller.get_motor_limit_switch(axis_id)
        if high:
            raise FlomniError("Fcapy in high limit. How did we get here?? Aborting.")
        if not low:
            self.ensure_osa_back()
            if dev.fcapy.readback.get() < -0.2:
                umv(dev.fcapy, -0.2)
            
            dev.fcapy.controller.drive_axis_to_limit(axis_id_numeric, "reverse")
            

    def ensure_gripper_up(self):
        axis_id = dev.ftransy._config["deviceConfig"].get("axis_Id")
        axis_id_numeric = self.axis_id_to_numeric(axis_id)
        low, high = dev.ftransy.controller.get_motor_limit_switch(axis_id)
        if low:
            raise FlomniError("Ftransy in low limit. How did we get here?? Aborting.")
        
        if high:
            return
        
        if dev.ftransy.readback.get() < -0.5:
            umv(dev.ftransy, -0.5)
        dev.ftransy.controller.drive_axis_to_limit(axis_id_numeric, "forward")
        

    def check_tray_in(self):
        axis_id = dev.ftray._config["deviceConfig"].get("axis_Id")
        low, high = dev.ftray.controller.get_motor_limit_switch(axis_id)
        if high:
            raise FlomniError("Ftray is in the 'OUT' position. Aborting.")
        
        if not low:
            raise FlomniError("Ftray is not at the 'IN' position. Aborting.")
        
        

    def ftransfer_flomni_stage_out(self):
        target_pos = -162
        if np.isclose(dev.fsamx.readback.get(), target_pos, 0.01):
            return
        
        umv(dev.fsamroy, 0)

        # TODO: disable rt feedback!!

        self.ensure_fcapy_up()

        self.ensure_gripper_up()

        self.check_tray_in()

        # TODO: laser track on
        time.sleep(0.05)
        fsamy_in = dev.fsamy.user_parameter.get("in")
        if fsamy_in is None:
            raise FlomniError("Could not find an 'IN' position for fsamy. Please check your config.")
        umv(dev.fsamy, fsamy_in)
        time.sleep(0.05)
        # TODO: laser track on
        time.sleep(0.05)
        # TODO: laser track off
        time.sleep(0.05)

        self.drive_axis_to_limit(dev.fsamx, "forward")
        dev.fsamx.limits = [-162, 0]
        dev.fsamx.controller.socket_put_confirmed("axspeed[4]=25*stppermm[4]")
        
        umv(dev.fsamx, target_pos)

    def check_sensor_connected(self):
        sensor_voltage_target = dev.ftransy.user_parameter.get("sensor_voltage")
        sensor_voltage = float(dev.ftransy.controller.socket_put_and_receive("MG@AN[1]").strip())

        if not np.isclose(sensor_voltage, sensor_voltage_target, 0.5):
            raise FlomniError(f"Sensor voltage is {sensor_voltage}, indicates an error. Aborting.")

    def ftransfer_get_sample(self, position:int):
        self.check_position_is_valid(position)

        self.check_tray_in()
        self.check_sensor_connected()

        sample_in_gripper = bool(float(dev.flomni_samples.sample_in_gripper.get()))
        if sample_in_gripper:
            raise FlomniError("The gripper does carry a sample. Cannot proceed getting another sample.")
        
        sample_signal = getattr(dev.flomni_samples.sample_placed, f"sample{position}")
        sample_in_position = bool(float(sample_signal.get()))
        if not sample_in_position:
            raise FlomniError(f"The planned pick position [{position}] does not have a sample.")
        
        user_input = input("Please confirm that there is currently no sample in the gripper. It would be dropped! [y/n]")
        if user_input == "y":
            print("good then")
        else:
            print("Stopping.")
            return
        
        self.ftransfer_gripper_move(position)

        self.ftransfer_controller_enable_mount_mode()
        if position == 0:
            sample_height = -45 + dev.fsamy.user_parameter.get("in")
            
        else:
            sample_height = -17.5
        dev.ftransy.controller.socket_put_confirmed(f"getaprch={sample_height:.1f}")
        dev.ftransy.controller.socket_put_confirmed("XQ#GRGET,3")
        
        print("The unmount process started.")

        time.sleep(1)
        while True:
            in_progress = bool(float(dev.ftransy.controller.socket_put_and_receive("MG mntprgs").strip()))
            if not in_progress:
                break
            self.ftransfer_confirm()
            time.sleep(1)
        self.ftransfer_controller_disable_mount_mode()
        self.ensure_gripper_up()

        signal_name = getattr(dev.flomni_samples.sample_names, f"sample{position}")
        self.flomni_modify_storage_non_interactive(100, 1, signal_name.get())
        self.flomni_modify_storage_non_interactive(position, 0, "-")

    def ftransfer_put_sample(self, position:int):
        self.check_position_is_valid(position)

        self.check_tray_in()
        self.check_sensor_connected()

        sample_in_gripper = bool(float(dev.flomni_samples.sample_in_gripper.get()))
        if not sample_in_gripper:
            raise FlomniError("The gripper does not carry a sample.")
        
        sample_signal = getattr(dev.flomni_samples.sample_placed, f"sample{position}")
        sample_in_position = bool(float(sample_signal.get()))
        if sample_in_position:
            raise FlomniError(f"The planned put position [{position}] already has a sample.")
        
        self.ftransfer_gripper_move(position)

        self.ftransfer_controller_enable_mount_mode()
        if position == 0:
            sample_height = -45 + dev.fsamy.user_parameter.get("in")
            
        else:
            sample_height = -17.5
        dev.ftransy.controller.socket_put_confirmed(f"mntaprch={sample_height:.1f}")
        dev.ftransy.controller.socket_put_confirmed("XQ#GRPUT,3")
        
        print("The mount process started.")

        time.sleep(1)
        while True:
            in_progress = bool(float(dev.ftransy.controller.socket_put_and_receive("MG mntprgs").strip()))
            if not in_progress:
                break
            self.ftransfer_confirm()
            time.sleep(1)
        self.ftransfer_controller_disable_mount_mode()
        self.ensure_gripper_up()

        sample_name = dev.flomni_samples.sample_in_gripper.get()
        self.flomni_modify_storage_non_interactive(100, 0, "-")
        self.flomni_modify_storage_non_interactive(position, 1, sample_name)

        # TODO: flomni_stage_in if position == 0
        # bec.queue.next_dataset_number += 1

    def ftransfer_sample_change(self, new_sample_position:int):
        self.check_tray_in()
        sample_in_gripper = dev.flomni_samples.sample_in_gripper.get()
        if sample_in_gripper:
            raise FlomniError("There is already a sample in the gripper. Aborting.")
        
        self.check_position_is_valid(new_sample_position)

        sample_placed = getattr(dev.flomni_samples.sample_placed, f"sample{new_sample_position}").get()
        if not sample_placed:
            raise FlomniError(f"There is currently no sample in position [{new_sample_position}]. Aborting.")
        
        sample_in_sample_stage = dev.flomni_samples.sample_placed.sample0.get()
        if sample_in_sample_stage:
            # find a new home for the sample...
            empty_slots = []
            for name, val in dev.flomni_samples.read().items():
                if not "flomni_samples_sample_placed_sample" in name:
                    continue
                if val.get("value") == 0:
                    empty_slots.append(int(name.split("flomni_samples_sample_placed_sample")[1]))
            if not empty_slots:
                raise FlomniError("There are no empty slots available. Aborting.")
            
            print(f"The following slots are empty: {empty_slots}.")
            
            while True:
                user_input = input(f"Where shall I put the sample? Default: [{empty_slots[0]}]")
                try:
                    user_input = int(user_input)
                    if not user_input in empty_slots:
                        raise ValueError
                    break
                except ValueError:
                    print("Please specify a valid number.")
                    continue
            
            self.check_position_is_valid(user_input)

            self.ftransfer_get_sample(0)
            self.ftransfer_put_sample(user_input)

        self.ftransfer_get_sample(new_sample_position)
        self.ftransfer_put_sample(0)
        

    def flomni_modify_storage(self, position:int, used:int):
        if used:
            name = input("What's the name of this sample?")
        else:
            name = "-"
        self.flomni_modify_storage_non_interactive(position, used, name)

    def flomni_modify_storage_non_interactive(self, position:int, used:int, name:str):
        if position == 100:
            dev.flomni_samples.sample_in_gripper.set(used)
            dev.flomni_samples.sample_in_gripper_name.set(name)
        else:
            signal = getattr(dev.flomni_samples.sample_placed, f"sample{position}")
            signal.set(used)
            signal_name = getattr(dev.flomni_samples.sample_names, f"sample{position}")
            signal_name.set(name)


    def check_position_is_valid(self, position:int):
        if 0 <= position < 21:
            return
        raise FlomniError(f"The given position number [{position}] is not in the valid range of 0-21. ")

    def ftransfer_controller_enable_mount_mode(self):
        dev.ftransy.controller.socket_put_confirmed("XQ#MNTMODE")
        time.sleep(0.5)
        if not self.ftransfer_controller_in_mount_mode():
            raise FlomniError("System not switched to mount mode. Aborting.")

    def ftransfer_controller_disable_mount_mode(self):
        dev.ftransy.controller.socket_put_confirmed("XQ#POSMODE")
        time.sleep(0.5)
        if self.ftransfer_controller_in_mount_mode():
            raise FlomniError("System is still in mount mode. Aborting.")

    def ftransfer_controller_in_mount_mode(self) -> bool:
        in_mount_mode = bool(float(dev.ftransy.controller.socket_put_and_receive("MG mntmod").strip()))
        return in_mount_mode

    def ftransfer_confirm(self):
        confirm = int(float(dev.ftransy.controller.socket_put_and_receive("MG confirm").strip()))

        if confirm != -1:
            return
        
        user_input = input("All OK? Continue? [y/n]")
        if user_input == "y":
            print("good then")
            dev.ftransy.controller.socket_put_confirmed("confirm=1")
        else:
            print("Stopping.")
            return

    def ftransfer_gripper_is_open(self) -> bool:
        status = bool(float(dev.ftransy.controller.socket_put_and_receive("MG @OUT[9]").strip()))
        return status

    def ftransfer_gripper_open(self):
        sample_in_gripper = dev.flomni_samples.sample_in_gripper.get()
        if sample_in_gripper:
            raise FlomniError("Cannot open gripper. There is still a sample in the gripper! Aborting.")
        if not self.ftransfer_gripper_is_open():
            dev.ftransy.controller.socket_put_confirmed("XQ#GROPEN,4")

    def ftransfer_gripper_close(self):
        if self.ftransfer_gripper_is_open():
            dev.ftransy.controller.socket_put_confirmed("XQ#GRCLOS,4")

    def ftransfer_gripper_move(self, position:int):

        self.check_position_is_valid(position)

        self._ftransfer_shiftx = -0.2
        self._ftransfer_shiftz = -0.5

        fsamx_pos = dev.fsamx.readback.get()
        if position == 0 and fsamx_pos > -160:
            user_input = input("May the flomni stage be moved out for the sample change? Feedback will be disabled and alignment will be lost! [y/n]")
            if user_input == "y":
                print("good then")
                self.ftransfer_flomni_stage_out()
            else:
                print("Stopping.")
                return
        
        self.ensure_gripper_up()
        self.check_tray_in()

        if position==0:
            umv(dev.ftransx, 10.715+0.2, dev.ftransz, 3.5950)
        if position==1:
            umv(dev.ftransx, 41.900+self._ftransfer_shiftx, dev.ftransz, 74.7500+self._ftransfer_shiftz)
        if position==2:
            umv(dev.ftransx, 31.900+self._ftransfer_shiftx, dev.ftransz, 74.7625+self._ftransfer_shiftz)
        if position==3:
            umv(dev.ftransx, 21.900+self._ftransfer_shiftx, dev.ftransz, 74.7750+self._ftransfer_shiftz)
        if position==4:
            umv(dev.ftransx, 11.900+self._ftransfer_shiftx, dev.ftransz, 74.7875+self._ftransfer_shiftz)
        if position==5:
            umv(dev.ftransx, 1.9000+self._ftransfer_shiftx, dev.ftransz, 74.8000+self._ftransfer_shiftz)
        if position==6:
            umv(dev.ftransx, 41.900+self._ftransfer_shiftx, dev.ftransz, 89.7500+self._ftransfer_shiftz)
        if position==7:
            umv(dev.ftransx, 31.900+self._ftransfer_shiftx, dev.ftransz, 89.7625+self._ftransfer_shiftz)
        if position==8:
            umv(dev.ftransx, 21.900+self._ftransfer_shiftx, dev.ftransz, 89.7750+self._ftransfer_shiftz)
        if position==9:
            umv(dev.ftransx, 11.900+self._ftransfer_shiftx, dev.ftransz, 89.7875+self._ftransfer_shiftz)
        if position==10:
            umv(dev.ftransx, 1.900+self._ftransfer_shiftx , dev.ftransz, 89.8000+self._ftransfer_shiftz)
        if position==11:
            umv(dev.ftransx, 41.95+self._ftransfer_shiftx, dev.ftransz, 124.75+self._ftransfer_shiftz)
        if position==12:
            umv(dev.ftransx, 31.95+self._ftransfer_shiftx, dev.ftransz, 124.7625+self._ftransfer_shiftz)
        if position==13:
            umv(dev.ftransx, 21.95+self._ftransfer_shiftx, dev.ftransz, 124.7750+self._ftransfer_shiftz)
        if position==14:
            umv(dev.ftransx, 11.95+self._ftransfer_shiftx, dev.ftransz, 124.7875+self._ftransfer_shiftz)
        if position==15:
            umv(dev.ftransx, 1.95+self._ftransfer_shiftx, dev.ftransz, 124.8000+self._ftransfer_shiftz)
        if position==16:
            umv(dev.ftransx, 41.95+self._ftransfer_shiftx, dev.ftransz, 139.7500+self._ftransfer_shiftz)
        if position==17:
            umv(dev.ftransx, 31.95+self._ftransfer_shiftx, dev.ftransz, 139.7625+self._ftransfer_shiftz)
        if position==18:
            umv(dev.ftransx, 21.95+self._ftransfer_shiftx, dev.ftransz, 139.7750+self._ftransfer_shiftz)
        if position==19:
            umv(dev.ftransx, 11.95+self._ftransfer_shiftx, dev.ftransz, 139.7875+self._ftransfer_shiftz)
        if position==20:
            umv(dev.ftransx, 1.95+self._ftransfer_shiftx, dev.ftransz, 139.8000+self._ftransfer_shiftz)




class Flomni(FlomniInitStagesMixin, FlomniSampleTransferMixin):

    def drive_axis_to_limit(self, device, direction):
        axis_id = device._config["deviceConfig"].get("axis_Id")
        axis_id_numeric = self.axis_id_to_numeric(axis_id)
        device.controller.drive_axis_to_limit(axis_id_numeric, direction)

    def axis_id_to_numeric(self, axis_id) -> int:
        return ord(axis_id.lower()) - 97


if __name__ == "__main__":
    from bec_client import BECIPythonClient
    bec = BECIPythonClient()
    bec.start()
    bec.load_high_level_interface("spec_hli")
    scans = bec.scans
    dev = bec.device_manager.devices
    flomni = Flomni()
    # flomni.ftransfer_sample_change(12)
    flomni.ftransfer_gripper_open()
    time.sleep(2)
    flomni.ftransfer_gripper_close()

