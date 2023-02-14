#! /usr/bin/env python

import argparse
import re
import sys

MAX_IPV4 = 2**32 - 1


def cidr_to_subnet(address: str, prefix: int):
    # convert cidr prefix to network mask:
    subnet_mask_dec = MAX_IPV4 ^ (MAX_IPV4 >> prefix)
    subnet_mask_bin = bin(subnet_mask_dec)[2:]
    subnet_mask_octets = [
        int(subnet_mask_bin[i * 8 : (i + 1) * 8], base=2) for i in range(4)
    ]
    subnet_mask_str = ".".join(map(str, subnet_mask_octets))
    address_count = 2 ** (32 - prefix)

    # find network id
    network_id_octets = []
    address_octets = [int(addr) for addr in address.split(".")]
    for address_octet, mask_octet in zip(address_octets, subnet_mask_octets):
        network_id_octets.append(address_octet & mask_octet)

    # find broadcast ip:
    #    network_id | ~subnetmask

    return {
        "subnet_mask": subnet_mask_str,
        "network_id": ".".join(map(str, network_id_octets)),
        "next_network": "blah",
        "broadcast_ip": "blah",
        "first_host": "blah",
        "last_host": "blah",
        "addressable_hosts": address_count - 2,
    }


if __name__ == "__main__":
    # validate input; # input should look like 123.123.123.123/24
    assert len(sys.argv) == 2
    address = sys.argv[1]
    pat = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(?:[1-9]|[12][0-9]|3[0-2])$"  # credit: https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch07s16.html
    )
    assert pat.match(address)
    ip, cidr_prefix = address.split("/")
    results = cidr_to_subnet(ip, int(cidr_prefix))
    print(results)
