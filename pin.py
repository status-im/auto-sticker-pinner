import logging

from pack import StickerPack, ipfsBinToText

LOG = logging.getLogger('root')

def pinAllPacks(ipfs, contract):
    # Get hashes of sticker packs the contract knows about
    pack_hashes = contract.getAllPackHashes()
    
    # Covert hashes into covert into more easily usable StickerPacks
    packs = [StickerPack(ipfsBinToText(h)) for h in pack_hashes]
    
    # Iterate over packs and make sure they are all pinned
    for pack in packs:
        LOG.info('Pinning: %s', pack)
        rval = ipfs.pin(pack.content_hash)
        for chash in pack.image_hashes:
            LOG.debug('Pinning image: %s', chash)
            pinned = ipfs.pin(chash)
            if pinned:
                LOG.debug('Successfully pinned: %s', chash)
            else:
                LOG.error('Failed to pin image: %s', chash)
