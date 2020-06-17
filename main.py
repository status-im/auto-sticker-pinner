#!/usr/bin/env python3

import web3
from web3 import Web3

# Local modules
from ipfs import IpfsPinner
from pin import pinAllPacks
from log import setup_custom_logger

def main():
    LOG = setup_custom_logger('root')

    LOG.info('Connecting to Geth RPC: %s', 'TODO')
    # web3 instance for talking to Geth RPC
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

    LOG.info('Connecting to IPFS Cluster: %s', 'TODO')
    # for talking to IPFS cluster and pinning images
    ipfs = IpfsPinner()

    LOG.info('Pinning all existing packs...')
    pinAllPacks(w3, ipfs)

    #block_filter = w3.eth.filter('latest')
    #log_loop(block_filter, 2)

if __name__ == '__main__':
    main()
