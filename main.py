#!/usr/bin/env python3

import web3
from web3 import Web3
from optparse import OptionParser

# Local modules
from ipfs import IpfsPinner
from pin import pinAllPacks
from log import setup_custom_logger

HELP_DESCRIPTION='This is a simple utility for cleaning ElasticSearch indices.'
HELP_EXAMPLE='Example: ./esclean.py -i "logstash-2019.11.*" -p beacon -d'

def parse_opts():
    parser = OptionParser(description=HELP_DESCRIPTION, epilog=HELP_EXAMPLE)
    parser.add_option('-I', '--log-level', default='INFO',
                      help='Level of logging.')
    
    return parser.parse_args()


def main():
    (opts, args) = parse_opts()

    LOG = setup_custom_logger('root', opts.log_level)

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
