#! /usr/bin/env python

import argparse
import re
import sys


def cidr_to_subnet(address, cidr):
    complement = 32 - cidr
    mask_len = complement % 8
    mask = 256 - mask_len
    octet = cidr // 8 + 1
    group_size = 2**complement

    if octet == 1:
        subnet_mask = f"{mask}.0.0.0"
    elif octet == 2:
        subnet_mask = f"255.{mask}.0.0"
    elif octet == 3:
        subnet_mask = f"255.255.{mask}.0"
    else:
        subnet_mask = f"255.255.255.{mask}"

    return {
        "subnet_mask": subnet_mask,
        "network_id": "blah",
        "next_network": "blah",
        "broadcast_ip": "blah",
        "first_host": "blah",
        "last_host": "blah",
        "addressable_hosts": group_size - 2,
    }


if __name__ == "__main__":
    # validate input; # input should look like 123.123.123.123/24
    assert len(sys.argv) == 2
    address = sys.argv[1]
    pat = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:[1-9]|[12][0-9]|3[0-2])$"  # credit: https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html
    )
    assert pat.match(address)
    ip, cidr = address.split("/")
    results = cidr_to_subnet(ip, cidr)
    print(results)
