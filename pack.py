class StickerPack:
    # https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1577.md
    # All content hashes in Sticker Pack metadata have the same prefix.
    content_hash_rgx = r'e30101701220\w+'

    def __init__(self, url):
        resp = requests.get(url)
        resp.raise_for_status()
        self.image_hashes = SticketPack.parse_clj_meta(resp.text)

    @staticmethod
    def parse_clj_meta(data):
        # Find all content hashes of images in the Clojure formatted metadata
        matches = re.findall(SticketPack.content_hash_rgx, data)
        # IPFS can't handle EIP-1577 content hashes
        return [content_hash.decode(ch) for ch in matches]