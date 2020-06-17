import json

from contract import StickerPackContract
from pack import StickerPack, ipfsBinToText

SPACK_CONTRACT = "0x0577215622f43a39F4Bc9640806DFea9b10D2A36"
with open("./abi.json", "r") as f:
    STICKER_PACK_ABI = json.load(f)

def pinAllPacks(w3, ipfs):
    # Get instance of sticker pack contract
    sPack = StickerPackContract(SPACK_CONTRACT, STICKER_PACK_ABI, w3)

    # Get hashes of sticker packs the contract knows about
    pack_hashes = sPack.getAllPackHashes()
    
    # Covert hashes into covert into more easily usable StickerPacks
    packs = [StickerPack(ipfsBinToText(h)) for h in pack_hashes]
    
    # Iterate over packs and make sure they are all pinned
    for pack in packs:
        print("pack:", pack)
        rval = ipfs.pin(pack.content_hash)
        for chash in pack.image_hashes:
            print('image:', chash)
            pinned = ipfs.pin(chash)
            if not pinned:
                print('failed to pin:', chash)
