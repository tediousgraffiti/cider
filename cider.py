#! /usr/bin/env python

import json
import re
import sys

MAX_IPV4 = 0b11111111_11111111_11111111_11111111


def byte_repr(num: int, padding=8) -> str:
    return f"{num:0{padding}b}"


def dotted_decimal_to_uint32(address: str) -> int:
    octets = map(int, address.split("."))
    binary_repr = "".join(byte_repr(octet) for octet in octets)
    return int(binary_repr, base=2)


def uint32_to_dotted_decimal(address: int) -> str:
    binary_repr = byte_repr(address, padding=32)
    octets = [str(int(binary_repr[i * 8 : (i + 1) * 8], base=2)) for i in range(4)]
    dotted_decimal = ".".join(octets)
    return dotted_decimal


def cidr_to_subnet(address: str, prefix: int):
    subnet_mask = MAX_IPV4 ^ (MAX_IPV4 >> prefix)
    network_id = dotted_decimal_to_uint32(address) & subnet_mask
    broadcast_ip = network_id | ~subnet_mask & 0xFFFF
    address_count = 2 ** (32 - prefix)

    return {
        "subnet_mask": uint32_to_dotted_decimal(subnet_mask),
        "network_id": uint32_to_dotted_decimal(network_id),
        "next_network": uint32_to_dotted_decimal(broadcast_ip + 1),
        "broadcast_ip": uint32_to_dotted_decimal(broadcast_ip),
        "first_host": uint32_to_dotted_decimal(network_id + 1),
        "last_host": uint32_to_dotted_decimal(broadcast_ip - 1),
        "addressable_hosts": address_count - 2,
    }


if __name__ == "__main__":
    assert len(sys.argv) == 2
    address = sys.argv[1]
    pat = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:[1-9]|[12][0-9]|3[0-2])$"  # credit: https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html
    )
    assert pat.match(address)

    ip, cidr_prefix = address.split("/")
    print(json.dumps(cidr_to_subnet(ip, int(cidr_prefix)), indent=4))
