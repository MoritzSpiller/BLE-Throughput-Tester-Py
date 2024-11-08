from bleak import BleakClient, BleakScanner
import asyncio
import logging

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.backends.characteristic import BleakGATTCharacteristic

logger = logging.getLogger(__name__)

# UUIDs Nordic Throughput Service
DEVICE_UUID = "12175CC3-79B6-0CAE-584B-2524E46EC07B"
SERVICE_UUID = "e9ea0001-e19b-482d-9293-c7907585fc48"
CHAR_UUID = "e9ea0002-e19b-482d-9293-c7907585fc48"

# Application parameters
TIME_RECEIVING = 30.0
BYTES_RECEIVED = 0


def device_found(device: BLEDevice, advertisement_data: AdvertisementData):
    """Callback when a device is found during scanning."""
    logger.info(f"{device.address} : {advertisement_data}")


def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """Notification handler which processes the data received."""
    global BYTES_RECEIVED
    BYTES_RECEIVED += len(data)


def calculate_throughput():
    """Calculate the throughput based on bytes received and time."""
    return BYTES_RECEIVED / TIME_RECEIVING


async def main():
    logger.info("Starting scan...")

    device = None

    try:
        devices = await BleakScanner.discover(
            return_adv=True,
            service_uuids=[SERVICE_UUID],
            cb=dict(use_bdaddr=False),
        )
        for d, a in devices.values():
            print(d)
            print("-" * len(str(d)))
            print(a)
            if SERVICE_UUID in a.service_uuids:
                device = d

        if device is None:
            logger.error("No device found with the specified service UUID.")
            return

        logger.info("Connecting to device...")
        notifiy_char = None

        async with BleakClient(device) as client:
            logger.info("Connected")

            for service in client.services:
                logger.info(f"Service UUID: {service.uuid}, Metadata: {service}")

                for characteristic in service.characteristics:
                    logger.info(f"Characteristic: {characteristic}, UUID: {characteristic.uuid}")
                    if characteristic.uuid == CHAR_UUID:
                        notifiy_char = characteristic
                        await client.start_notify(characteristic, notification_handler)

            await asyncio.sleep(TIME_RECEIVING)
            await client.stop_notify(notifiy_char)
            await client.disconnect()

        throughput = calculate_throughput()
        logger.info(f"Calculated throughput: {throughput} bytes per second")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    print("Finish program")


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

    asyncio.run(main())
