from illumio.firewall import Firewall
from random import randint, choice
from pathlib import Path

import time


def generate_random_case():
    direction_ = choice(["inbound", "outbound"])
    protocol_ = choice(["tcp", "udp"])
    port_ = randint(1, 65536)
    ip_address_ = "{}.{}.{}.{}".format(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
    return direction_, protocol_, port_, ip_address_


def test_basic() -> None:

    fw = Firewall("tests/cases/sample_rules.csv")

    assert fw.accept_packet("inbound", "tcp", 80, "192.168.1.2") is True
    assert fw.accept_packet("inbound", "udp", 53, "192.168.2.1") is True
    assert fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11") is True
    assert fw.accept_packet("inbound", "tcp", 81, "192.168.1.2") is False
    assert fw.accept_packet("inbound", "udp", 24, "52.12.48.92") is False


def test_all_allowed() -> None:
    fw = Firewall("tests/cases/all_allowed.csv")

    # Test with 1000 random cases
    for case in range(1000):
        direction, protocol, port, ip_address = generate_random_case()
        assert fw.accept_packet(direction, protocol, port, ip_address) is True


def test_large_file() -> None:
    large_file_path = "tests/cases/large_file.csv"
    with open(large_file_path, "w") as f:

        for i in range(0, 500000):
            direction, protocol, port, ip_address = generate_random_case()
            f.write("{},{},{},{}".format(direction, protocol, port, ip_address))
            f.write("\n")

        # Write a verifiable entry at the end
        f.write("inbound,tcp,22,10.10.10.10")

    fw = Firewall("tests/cases/large_file.csv")

    start = time.monotonic()

    assert fw.accept_packet("inbound", "tcp", 22, "10.10.10.10") is True

    time_taken = time.monotonic() - start

    # Test time taken is reasonable.
    assert time_taken < 5

    # Delete the file
    Path(large_file_path).unlink()