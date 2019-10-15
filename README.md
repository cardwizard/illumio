# Illumio
Pure python implementation of a Firewall class.
`Python > 3.5`

## Usage
```python
from illumio.firewall import Firewall
fw = Firewall("/path/to/firewall.csv")
fw.accept_packet("inbound", "tcp", 80, "192.168.1.2")
```
firewall.csv contains line separated rules in the following format:

```csv
direction,protocol,port(port-range),ip(ip-range)
inbound,tcp,80,192.168.1.2
outbound,tcp,10000-20000,192.168.10.11
inbound,udp,53,192.168.1.1-192.168.2.5
outbound,udp,1000-2000,52.12.48.92
```

## Project organization
The project is organized as follows: 

    - illumio
        - __init__.py
        - firewall.py: Firewall class
        - datastructs.py: Helper datastructures
    - tests
        - cases
            - all_allowed.csv: Edge case where everything is allowed
            - sample_rules.csv: Contains a few rules to test the firewall against
            - nothing_allowed.csv: This is empty. :P
             
        - test_firewall.py: Contains basic tests for different cases 
    
    - runner.py: A file to quickly run and check any cases
        

## Design choices
1. **Chain Rule**: The API for accept_packet takes inspiration from the chain rule in numpy. The filters can be chained to create a bigger filter. Every filter accepts self and returns the same object class to make this possible.   
You can find the implementation in the `accept_packet` function of the `Firewall` class in `firewall.py`. This design choice will allow easy implementation and quick scaling. Also, in case we know which search space is the most sparse we can reorder our filters to get faster performance. 
```python
filtered_rules = self.rules.filter_by_dp_index(direction, protocol).filter_by_port(port).filter_by_ip(ip_address)
```
2. **Direction-Protocol Index**: I only had enough time to create a quick index on direction and protocol. Since the number of directions and protocols will be limited, the directory protocol index contains lists of IDs which match the given protocol and direction.
The first filtering is based on this index. This (in average case) should reduce our search space to 1/4th of the original search space.
The index is not memory heavy since it just saves the IDs.

3. **ID-Rule reverse index**: I also maintain a reverse index to map back to the ID once the directory-protocol search is done.  

4. **Standardizing the port range and IP range**: Maintaining both single numbers for ports and ranges was too much of an hassle. Instead, we can convert everything to a range.
In my implementation, I convert a number (say, num) to a range [num-num]. This makes the implementation easier and removes unnecessary cases from the codebase. The same logic applies for IP addresses.
## Tests
### Running the tests
Navigate to the outermost directory and run
```
pytest .
```

## Future optimizations

The search in the port range and IP range is pretty basic as of now and has a lot of potential for improvement. A simple numpy filtering itself can improve the performance by orders of magnitude. Other optimization ideas are:

    - Sorting the ports/IPs by their end range and using binary search to narrow down the range.
    - Parallelly searching for the ranges using threads (Python has amazing support in JobLib)
    - Automatically reordering the filters to find the optimal search pattern.
    - Matching multiple rules at the same time in the accept_packet function.
    - A simpler way would be to use an inmemory database (like sqlite3 or redis) and use filtering mechanisms that the database folks have built.
    
## Team Interests
  - Data Team
  - Platform Team