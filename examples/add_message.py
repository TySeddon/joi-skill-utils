import random
from joi_skill_utils.joiclient import JoiClient
from joi_skill_utils.enviro import get_setting

device_id = get_setting("device_id")
client = JoiClient(device_id)
resident = client.get_Resident()

client.add_DeviceMessage_Me(message={"action":"test"})

