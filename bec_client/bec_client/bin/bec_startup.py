###############################################################
####### INITIALIZE THE BEC CLIENT - DO NOT MODIFY #############
###############################################################
from bec_utils import RedisConnector, ServiceConfig, bec_logger

from bec_client import BECClient

# pylint: disable=wrong-import-position
# pylint: disable=protected-access

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.SUCCESS

CONFIG_PATH = "../bec_config.yaml"

config = ServiceConfig(CONFIG_PATH)

bec = BECClient()
bec.initialize(config.redis, RedisConnector, config.scibec)
bec.start()
bec.load_high_level_interface("spec_hli")

dev = bec.device_manager.devices
scans = bec.scans

####################### END OF INIT #############################

# MODIFY THE SECTIONS BELOW TO CUSTOMIZE THE BEC

################################################################
################################################################

# SETUP BEAMLINE INFO
from bec_client.plugins.cSAXS.beamline_info import BeamlineInfo
from bec_client.plugins.SLS.sls_info import OperatorInfo, SLSInfo

bec._bl_info_register(BeamlineInfo)
bec._bl_info_register(SLSInfo)
bec._bl_info_register(OperatorInfo)

# SETUP CLIENT PLUGINS
# from bec_client.plugins.cSAXS import fshclose, fshopen, fshstatus
