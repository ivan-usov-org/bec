from bec_lib import MessageEndpoints
from bec_lib.serialization import MsgpackSerialization

def load_last_camera_data(count:int) -> list:
    """
    Load the last <count> entries of the camera data monitor stream. 

    Args:
        count (int): number of images to retrieve
    
    Returns:
        list: List of numpy arrays
    """
    im = bec.connector._redis_conn.xrevrange(MessageEndpoints.device_monitor("camera").endpoint,"+", "-", count=count)
    im = [{k.decode(): MsgpackSerialization.loads(msg) for k, msg in sub_img[1].items()}["data"].data for sub_img in im]
    return im


