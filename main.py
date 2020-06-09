#!/usr/bin/env python3

import json
import web3
from web3 import Web3

# Local modules
from ipfs import IpfsPinner
from pack import StickerPack, ipfsBinToText
from contract import StickerPackContract

STICKER_PACK_CONTRACT = "0x0577215622f43a39F4Bc9640806DFea9b10D2A36"
with open("./abi.json", "r") as f:
    STICKER_PACK_ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

s = StickerPackContract(STICKER_PACK_CONTRACT, STICKER_PACK_ABI, w3)

pack_hashes = s.getAllPackHashes()

packs = [StickerPack(ipfsBinToText(h)) for h in pack_hashes]
print(packs)
