import re
import json
import requests
import multiaddr
import content_hash # https://pypi.org/project/content-hash
import ipfscluster  # https://pypi.org/project/ipfscluster

# Converts binary content hash to text verison, see EIP-1577
def ipfsBinToText(text):
    return content_hash.decode(text)

class IpfsPinner:
    

    def __init__(self, addr='/dns/localhost/tcp/9094/http'):
        self.address = multiaddr.Multiaddr(addr)     
        self.cluster = ipfscluster.connect(addr)

    def statuses(self, chash):
        return [
            peer['status'] for
            peer in self.ls(chash)['peer_map'].values()
        ]

    # See: https://cluster.ipfs.io/documentation/guides/pinning/
    def status(self, chash):
        statuses = self.statuses(chash)
        if all(s == 'pinned' for s in statuses):
            return 'pinned'
        elif all(s == 'unpinned' for s in statuses):
            return 'unpinned'
        elif all(s == 'pinning' for s in statuses):
            return 'pinning'
        elif all(s == 'pin_queued' for s in statuses):
            return 'pin_queued'
        elif all(s == 'pin_error' for s in statuses):
            return 'failed'
        elif any(s == 'pin_error' for s in statuses):
            return 'errors'
        else:
            return 'mixed'

    def is_pinned(self, chash):
        statuses = self.statuses(chash)
        return all(s == 'pinned' for s in statuses)

    def pin(self, chash):
        if self.is_pinned(chash):
            return 'pinned'

        rval = self.cluster.pins.add(chash)
        return self.status(chash)

    def ls(self, chash):
        return self.cluster.pins.ls(chash)
