from illumio import Firewall

if __name__ == '__main__':
    fw = Firewall("/path/to/csv")

    assert fw.accept_packet("inbound", "tcp", 80, "192.168.1.2") is True
    assert fw.accept_packet("inbound", "udp", 53, "192.168.2.1") is True
    assert fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11") is True
    assert fw.accept_packet("inbound", "tcp", 81, "192.168.1.2") is False
    assert fw.accept_packet("inbound", "udp", 24, "52.12.48.92") is False
