# 	• initialize:
# 		○ server loads config from disk and sends it Kafka
# 		○ OPAAS confirms it and sends new config to Kafka
# 		○ client, server and OPAAS read new config
# 	• move motor
# 		○ client requests mvr(motor1, 5) and sends it to scan queue
# 		○ server reads from scan queue and pushes instructions to device_instructions
#          OPAAS reads from device instructions, performs action and sends readback to device_<id>

from bec_utils import RedisConnector, ServiceConfig, bec_logger

from bec_client import BKClient

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.SUCCESS

CONFIG_PATH = "../bec_config.yaml"


config = ServiceConfig(CONFIG_PATH)

bk = BKClient(
    [config.redis],
    RedisConnector,
    config.scibec,
)
bk.start()
bk.load_high_level_interface("spec_hli")

dev = bk.devicemanager.devices
scans = bk.scans

logger.success("Started BKClient")
# scans.fermat_scan(dev.samx, -2, 2, dev.samy, -2, 2, step=1.5, exp_time=0.02, relative=True)
# dev.samx.low_limit = -20
# scans.round_scan_fly(dev.samx, dev.samy, 0, 50, 20, 3, exp_time=0.1, relative=True)
# def plotfunc():
#     dp = PlotAxis(bk.devicemanager.connector)
#     dp.start()

# scans.umv(dev.samx, 10, relative=True)

# scans.mv(dev.samx, 20, dev.samy, -20)
# s = scans.line_scan(dev.samy, -5, 40, steps=10, exp_time=0.1)
# s = scans.round_roi_scan(dev.samx, 50, dev.samy, 20, dr=2, nth=3, exp_time=0.1)

# scan_def_id = str(uuid.uuid4())
# scans.open_interactive_scan(dev.samx, dev.samy, exp_time=0.1, md={"scan_def_id": scan_def_id})
# for ii in range(5):
#     scans.mv(dev.samx, ii, dev.samy, ii + 3, md={"scan_def_id": scan_def_id})
#     scans.interactive_scan_trigger(dev.samx, dev.samy, md={"scan_def_id": scan_def_id})
# scans.close_interactive_scan(md={"scan_def_id": scan_def_id})


# @scan_def
# def new_scan():
#     for ii in range(10):
#         scans.umv(dev.samx, ii * 10)
#         scans.fermat_scan(dev.samx, -5, 5, dev.samy, -5, 5, step=1, exp_time=0.02, relative=True)


# for ii in range(10):
#     scans.umv(dev.samx, ii * 10)
#     # scans.grid_scan(dev.samx, -5, 5, 5, dev.samy, -5, 5, 10, exp_time=0.02, relative=True)
#     scans.fermat_scan(dev.samx, -5, 5, dev.samy, -5, 5, step=1, exp_time=0.02, relative=True)

# scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02)
# s = scans.grid_scan(dev.samx, -5, 5, 100, dev.samy, -5, 5, 100, exp_time=0.0, hide_report=True)
# scans.umv(dev.samx, 0)
# scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02)

# with scans.scan_def:
#     scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1)
#     scans.line_scan(dev.samx, -8, 8, steps=10, exp_time=0.1)


# scan_def_id = str(uuid.uuid4())
# scans.open_scan_def(md={"scan_def_id": scan_def_id})
# scans.line_scan(dev.samx, -5, 5, steps=10, exp_time=0.1, md={"scan_def_id": scan_def_id})
# scans.line_scan(dev.samx, -8, 8, steps=10, exp_time=0.1, md={"scan_def_id": scan_def_id})
# scans.close_scan_def(md={"scan_def_id": scan_def_id})
# for ii in range(10):
#     scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.01)

# res = dev.samx.read()
# dev.samx.summary()
# res = dev.samx.read(cached=True, use_readback=True).get("value")
# scans.umv(dev.samx, 500)
# print(dev.samx.read(cached=True, use_readback=True))
# scans.umv(dev.samx, 1000)


# @scans.scan_group
# def alignment(*args, **kwargs):
#     scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02)
#     scans.umv(dev.samx, 10)
#     scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02)
#     scans.umv(dev.samx, 10)
#     scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02)


# with scans.scan_group:
#     scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02)
#     scans.umv(dev.samx, 10)

# alignment()


# scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02, md={"queue_group": queue_group})
# scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=0.02, md={"queue_group": queue_group})

# scans.grid_scan(dev.samx, -5, 5, 10, dev.samy, -5, 5, 10, exp_time=1)

# event = threading.Event()
# event.wait()
print("eos")
# p.join()
