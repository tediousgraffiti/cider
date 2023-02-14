# Cider

## Description

IPv4 CIDR notation subnet calculator.

Give it a CIDR and it'll report the network details. Alternatively, give it an ip range as start and end and it'll give you the relevant CIDR.

Future work might include suggesting networks from simple inputs.

Update: lol of course this is [built into the standard library](https://docs.python.org/3/library/ipaddress.html)...Alright, will have to do two passes, one the hard way, one with the provided batteries. Key idea there seems to be to convert everything to big'ol 32 bit integers and do all the operations there before converting back.

## References

* [Practical Networking - Subnetting Mastery](https://www.youtube.com/watch?v=BWZ-MHIhqjM&list=PLIFyRwBY_4bQUE4IB5c4VPRyDoLgOdExE&index=2&ab_channel=PracticalNetworking)
* [identify network and broadcast address of a subnet](https://www.countryipblocks.net/blog/identifying-the-network-and-broadcast-address-of-a-subnet/)
* [ipaddress.py source](https://github.com/python/cpython/blob/4aeae286715a3a9fa624429733582917606000c3/Lib/ipaddress.py)
