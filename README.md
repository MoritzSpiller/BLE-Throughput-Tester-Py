Sure! Here's a short `README.md` for your code:

# BLE Throughput Measurement

This project measures the throughput of a Bluetooth Low Energy (BLE) device using the Nordic Throughput Service.

## Requirements

- Python 3.7+
- bleak library

Install the required library using pip:

```bash
pip install bleak
```

## Usage

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MoritzSpiller/BLE-Throughput-Tester-Py.git  
    cd BLE-Throughput-Tester
    ```

2. **Run the script**:
    ```bash
    python main.py
    ```

## Code Overview

- `device_found(device, advertisement_data)`: Callback function when a device is found during scanning.
- `notification_handler(characteristic, data)`: Handles notifications and processes the received data.
- `calculate_throughput()`: Calculates the throughput based on bytes received and time.
- `main()`: Main function to scan for devices, connect to the target device, and measure throughput.

## Logging

The script uses Python's `logging` module to log information. The log level is set to `INFO` by default.

## License

This project is licensed under the MIT License.