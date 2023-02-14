#! /usr/bin/env python

import argparse
import re
import sys

MAX_IPV4 = 2**32 - 1


def cidr_to_subnet(address: str, prefix: int):
    subnet_mask_dec = MAX_IPV4 ^ (MAX_IPV4 >> prefix)
    subnet_mask_bin = bin(subnet_mask_dec)[2:]
    subnet_mask_str = ".".join(
        map(
            lambda x: str(int(x, base=2)),
            (subnet_mask_bin[i * 8 : (i + 1) * 8] for i in range(4)),
        )
    )

    host_count = 2 ** (32 - prefix)

    # address_dec = address.split(".")
    # network_id = address ^ subnet_mask_bin

    # complement = 32 - prefix
    # mask_len = complement % 8
    # mask = 256 - mask_len
    # octet = cidr // 8 + 1
    # group_size = 2**complement

    # if octet == 1:
    #     subnet_mask = f"{mask}.0.0.0"
    # elif octet == 2:
    #     subnet_mask = f"255.{mask}.0.0"
    # elif octet == 3:
    #     subnet_mask = f"255.255.{mask}.0"
    # else:
    #     subnet_mask = f"255.255.255.{mask}"
    group_size = 42
    return {
        "subnet_mask": subnet_mask_str,
        "network_id": "blah",
        "next_network": "blah",
        "broadcast_ip": "blah",
        "first_host": "blah",
        "last_host": "blah",
        "addressable_hosts": host_count - 2,
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
