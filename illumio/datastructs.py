from ipaddress import IPv4Address
from typing import List, Dict


class Rule:
    def __init__(self, id, rule) -> None:
        self.id = id

        direction, protocol, port_range, ip_range = rule.split(",")
        self.direction = direction
        self.protocol = protocol

        # Standardize all port and range information. If it is a range, store it in
        # respective _start and _end variables. If it is a single port number or single address,
        # make _start and _end equal.
        self.port_range_start, self.port_range_end = Rule._split(str(port_range))

        ip_range_start, ip_range_end = Rule._split(str(ip_range))
        self.ip_range_start = IPv4Address(ip_range_start)
        self.ip_range_end = IPv4Address(ip_range_end)

    @staticmethod
    def _split(range_: str):
        if "-" in range_:
            range_ = range_.split("-")
            start = range_[0]
            end = range_[1]
            return start, end
        else:
            return range_, range_


class RuleList:
    def __init__(self, rules: List, create_dp_index: bool = False) -> None:
        self.rule_list = rules

        self.direction_protocol_index = {}

        if create_dp_index:
            self.direction_protocol_index = RuleList._create_dp_index(rules)

    def append(self, rule: Rule) -> None:
        """
        Helper functions to make it easy to use RuleList.
        """
        self.rule_list.append(rule)

    def get(self, id) -> Rule:
        """
        Function to fetch an object from a memory location
        """
        return self.rule_list[id]

    @staticmethod
    def _create_dp_index(rules: List) -> Dict:
        """
        Helper function to create a direction-protocol index to filter the first layer easily.
        This index is created only on the first call of the function.
        """
        dp_index = {}

        for rule in rules:
            if dp_index.get(rule.direction) is None:
                dp_index[rule.direction] = {}

            if dp_index[rule.direction].get(rule.protocol) is None:
                dp_index[rule.direction][rule.protocol] = []

            dp_index[rule.direction][rule.protocol].append(rule.id)

        return dp_index

    def _filter_by_id(self, id_list) -> List:
        """
        Helper function to extract rules given an ID list.
        """
        rules = [self.get(id) for id in id_list]
        return rules

    def filter_by_dp_index(self, direction: str, protocol: str):
        """
        Helper function to filter by both direction and protocol. Returns RuleList
        """
        dp_list = self.direction_protocol_index.get(direction, {}).get(protocol, [])
        return RuleList(self._filter_by_id(dp_list))

    def filter_by_port(self, port):
        """
        Helper function to filter by port.
        TODO: Can be optimized by sorting and searching over the sorted dataset / using a tree. Filter operations
              are great candidates for optimization through parallel processing. Simple numpy .filter operations can
              also give this a 10 times boost.
        """
        rules = list(filter(lambda x: int(x.port_range_start) <= int(port) <= int(x.port_range_end), self.rule_list))
        return RuleList(rules)

    def filter_by_ip(self, ip):
        """
        Helper function to filter by IP
        TODO: Can be optimized by sorting and searching over the sorted dataset / using a tree. Filter operations
              are great candidates for optimization through parallel processing
        """
        rules = list(filter(lambda x: x.ip_range_start <= IPv4Address(ip) <= x.ip_range_end, self.rule_list))
        return RuleList(rules)

    def matches(self):
        """
        Function to check if there is any rule that has matched so far.
        """
        if not self.rule_list:
            return False
        return True
