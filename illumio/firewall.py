from pathlib import Path
from illumio.datastructs import Rule, RuleList
from typing import List, Dict


class Firewall:
    def __init__(self, path_to_csv: str) -> None:
        """
        Initialize the Firewall class

        :param path_to_csv: Path to the csv containing rules in the format
            inbound,tcp,80,192.168.1.2
            outbound,tcp,10000-20000,192.168.10.11
            inbound,udp,53,192.168.1.1-192.168.2.5
            outbound,udp,1000-2000,52.12.48.92
        """
        self.path = Path(path_to_csv)

        if not self.path.exists():
            raise Exception("File {} not found".format(self.path))

        with open(self.path, "r") as f:
            rules = f.read().splitlines()

        # Process rules and store them as a RuleList object
        self.rules = Firewall._preprocess(rules)

    def accept_packet(self, direction: str, protocol: str, port: int, ip_address) -> bool:
        """
        Uses chain rule to filter by different parameters.
        Direction and protocol has been clubbed into 1.
        """

        filtered_rules = self.rules.filter_by_dp_index(direction, protocol).filter_by_port(port).filter_by_ip(ip_address)

        # Check if it matches any rule
        if filtered_rules.matches():
            return True

        return False

    @staticmethod
    def _parse_rule_object(id: int, rule: str):
        # Helper function to create a rule object
        return Rule(id, rule)

    @staticmethod
    def _preprocess(rules) -> RuleList:
        """
        Create a RuleList from a list of rules
        """
        processed_rules = []

        for id, rule in enumerate(rules):
            processed_rules.append(Firewall._parse_rule_object(id, rule))

        return RuleList(processed_rules, create_dp_index=True)
