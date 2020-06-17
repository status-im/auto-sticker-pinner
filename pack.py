import re
import requests
import logging

from ipfs import ipfsBinToText

LOG = logging.getLogger('root')

IPFS_GATEWAY = "https://cloudflare-ipfs.com/ipfs"

class StickerPack:
    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1577.md
    # All content hashes in Sticker Pack metadata have the same prefix.
    content_hash_rgx = r'e30101701220\w+'

    def __init__(self, chash):
        self.content_hash = chash

        resp = requests.get("{}/{}".format(IPFS_GATEWAY, chash))
        resp.raise_for_status()

        self.image_hashes = StickerPack.parse_clj_meta(resp.text)

    @staticmethod
    def parse_clj_meta(data):
        # Find all content hashes of images in the Clojure formatted metadata
        matches = re.findall(StickerPack.content_hash_rgx, data)
        # IPFS can't handle EIP-1577 content hashes
        return [ipfsBinToText(ch) for ch in matches]

    def __repr__(self):
        return '<Pack hash={} imgs={}>'.format(
            self.content_hash, len(self.image_hashes))

    def pin(self, ipfs):
        LOG.info('Pinning: %s', self)
        for chash in self.image_hashes + [self.content_hash]:
            LOG.debug('Pinning hash: %s', chash)
            pinned = ipfs.pin(chash)
            if pinned:
                LOG.debug('Successfully pinned: %s', chash)
            else:
                LOG.error('Failed to pin image: %s', chash)
