import spidev

def test_spi(bus, device):
    spi = spidev.SpiDev()
    spi.open(bus, device)
    spi.max_speed_hz = 1000000
    try:
        response = spi.xfer2([0x00])
        print(f"SPI response: {response}")
    finally:
        spi.close()

if __name__ == "__main__":
    SPI_BUS = 0  # SPI0
    SPI_DEVICE = 0  # CE0

    print("Testing SPI connection...")
    test_spi(SPI_BUS, SPI_DEVICE)