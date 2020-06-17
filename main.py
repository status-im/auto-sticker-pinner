#!/usr/bin/env python3

import web3
import json
from web3 import Web3
from optparse import OptionParser

# Local modules
from ipfs import IpfsPinner
from pin import pinAllPacks
from log import setup_custom_logger
from watch import ContractWatcher
from contract import StickerPackContract

HELP_DESCRIPTION='Utility for pinning images from Status Sticker packs.'
HELP_EXAMPLE='Example: ./main.py -TODO'

def parse_opts():
    parser = OptionParser(description=HELP_DESCRIPTION, epilog=HELP_EXAMPLE)

    parser.add_option('-g', '--geth-addr', default='http://localhost:8545',
                      help='IPFS Cluster API URL.')
    parser.add_option('-i', '--ipfs-addr', default='/dns/localhost/tcp/9094/http',
                      help='IPFS Cluster API MultiAddress.')
    parser.add_option('-p', '--pin-all', default=False,
                      help='If all packs should be pinned on start.')
    parser.add_option('-e', '--events', default=['ContenthashChanged', 'Register'],
                      help='Contract events to watch for.')
    parser.add_option('-c', '--contract', default='0x0577215622f43a39F4Bc9640806DFea9b10D2A36',
                      help='Sticker Pack contract address.')
    parser.add_option('-I', '--log-level', default='INFO',
                      help='Level of logging.')

    return parser.parse_args()


def main():
    (opts, args) = parse_opts()

    LOG = setup_custom_logger('root', opts.log_level)

    LOG.info('Connecting to Geth RPC: %s', opts.geth_addr)
    # web3 instance for talking to Geth RPC
    w3 = Web3(Web3.HTTPProvider(opts.geth_addr))

    LOG.info('Connecting to IPFS Cluster: %s', opts.ipfs_addr)
    # for talking to IPFS cluster and pinning images
    ipfs = IpfsPinner(opts.ipfs_addr)

    # Read Sticker Pack contract ABI
    with open("./abi.json", "r") as f:
        contract_abi = json.load(f)

    # Get instance of sticker pack contract
    contract = StickerPackContract(opts.contract, contract_abi, w3)

    if opts.pin_all:
        LOG.info('Pinning all existing packs...')
        pinAllPacks(ipfs, contract)

    global watcher
    LOG.info('Watching for events: %s', opts.events)
    watcher = ContractWatcher(w3, ipfs, contract)
    watcher.loop(opts.events)

if __name__ == '__main__':
    main()
