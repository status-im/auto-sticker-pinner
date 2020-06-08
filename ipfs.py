import re
import json
import requests
import content_hash # https://pypi.org/project/content-hash
import ipfscluster  # https://pypi.org/project/ipfscluster

# TODO parametrize
IPFS_CLUSTER_ADDR = 'http://localhost:9094'

# TODO parametrize
STICKER_PACKS_META_URLS = [
  "https://cloudflare-ipfs.com/ipfs/QmWVVLwVKCwkVNjYJrRzQWREVvEk917PhbHYAUhA1gECTM",
  "https://cloudflare-ipfs.com/ipfs/QmWpG2Q5NB472KLgFysdCjB8D1Qf9hxR2KNJvtCJQJufDj",
]

class IpfsPinner:

    def __init__(self, addr=ipfscluster.DEFAULT_ADDR):
        self.client = ipfscluster.connect(addr)

    def is_pinned(self, chash):
        resp = self.client.pins.ls(chash)
        statuses = [peer['status'] for peer in resp['peer_map'].values()]
        return all(s == 'pinned' for s in statuses), statuses

    def pin(self, chash):
        return self.client.pins.add(chash)
