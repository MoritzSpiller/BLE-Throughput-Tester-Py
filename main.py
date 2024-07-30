from bleak import BleakClient, BleakScanner
import asyncio
import logging

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.backends.characteristic import BleakGATTCharacteristic

logger = logging.getLogger(__name__)

# UUIDs Nordic Throughput Service
DEVICE_UUID = "12175CC3-79B6-0CAE-584B-2524E46EC07B"
SERVICE_UUID = "0483dadd-6c9d-6ca9-5d41-03ad4fff4abb"
CHAR_UUID = "00001524-0000-1000-8000-00805f9b34fb"

# Application parameters
TIME_RECEIVING = 10.0
BYTES_RECEIVED = 0

# TARGET_UUID = []

def device_found(device: BLEDevice, advertisement_data: AdvertisementData):
    logger.info("{} : {}".format(device.address, advertisement_data))


def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    global BYTES_RECEIVED
    """Simple notification handler which prints the data received."""
    logger.info("%s: %r", characteristic.description, data)
    BYTES_RECEIVED = BYTES_RECEIVED + len(bytearray)


def calculate_throughput():
    return (BYTES_RECEIVED / TIME_RECEIVING)


async def main():
    logger.info("starting scan...")

    devices = await BleakScanner.discover(
        return_adv=True,
        service_uuids=[SERVICE_UUID,],
        cb=dict(use_bdaddr=False),
    )
    for d, a in devices.values():
        print()
        print(d)
        print("-" * len(str(d)))
        print(a)
        if a.service_uuids[0] == SERVICE_UUID:
            device = DEVICE_UUID

    logger.info("connecting to device...")

    async with BleakClient(device) as client:
        logger.info("Connected")

        for service in client.services:
            logger.info("service uuid '%s', metadata: '%s", service.uuid, service)

            for characteristic in service.characteristics:
                logger.info("characteristic: %s; uuid: '%s", characteristic, characteristic.uuid)

            # value = await client.read_gatt_char(CHAR_UUID)
            # print(value)

        await asyncio.sleep(600.0)

    throughput = calculate_throughput()
    logger.info("Calculated throughput: {}".format(throughput))
    print("finish program")


if __name__ == '__main__':
    log_level = logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main())
