import re
import json
import requests
import content_hash # https://pypi.org/project/content-hash
import ipfscluster  # https://pypi.org/project/ipfscluster

# Converts binary content hash to text verison, see EIP-1577
def ipfsBinToText(text):
    return content_hash.decode(text)

class IpfsPinner:
    

    def __init__(self, addr=ipfscluster.DEFAULT_ADDR):
        self.cluster = ipfscluster.connect(addr)

    def statuses(self, chash):
        return [
            peer['status'] for
            peer in self.ls(chash)['peer_map'].values()
        ]

    def is_pinned(self, chash):
        return all(s == 'pinned' for s in self.statuses(chash))

    def pin(self, chash):
        if self.is_pinned(chash):
            return True

        rval = self.cluster.pins.add(chash)
        return self.is_pinned(chash)

    def ls(self, chash):
        return self.cluster.pins.ls(chash)
