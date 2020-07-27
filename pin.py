import logging

from pack import StickerPack, ipfsBinToText

LOG = logging.getLogger('root')

def pinAllPacks(ipfs, contract):
    LOG.debug('Querying contract for pack hashes...')
    # Get hashes of sticker packs the contract knows about
    pack_hashes = contract.getAllPackHashes()
    
    LOG.debug('Converting pack hashes...')
    # Covert hashes into covert into more easily usable StickerPacks
    packs = [StickerPack(ipfsBinToText(h)) for h in pack_hashes]
    
    # Iterate over packs and make sure they are all pinned
    for pack in packs:
        pack.pin(ipfs)
