from amcrest import AmcrestCamera
import socket
from contextlib import closing
from joi_skill_utils.camera_finder import CameraFinder
from joi_skill_utils.enviro import get_setting

# manual test of single known ip
__RTSP_PORT = 554
__PWGPSI_PORT = 3800
__HTTP_PORT = 80
ipaddr = "192.168.1.31"
with closing(socket.socket()) as sock:
    sock.connect((ipaddr, __RTSP_PORT))
with closing(socket.socket()) as sock:
    sock.connect((ipaddr, __HTTP_PORT))
# with closing(socket.socket()) as sock:
#     sock.connect((ipaddr, __PWGPSI_PORT))


# scan current network for camera of given name
CAMERA_NAME = get_setting('camera_name')
CAMERA_USERNAME = get_setting('camera_username')
CAMERA_PASSWORD = get_setting('camera_password')
finder = CameraFinder(CAMERA_NAME, CAMERA_USERNAME, CAMERA_PASSWORD)
found_devices = finder.scan_devices()
print(found_devices)
