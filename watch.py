import time
import logging

from pack import StickerPack, ipfsBinToText

LOG = logging.getLogger('root')

def getAllEvents(event_filters):
    return [
        log
        for ev_filter in event_filters
        for log in ev_filter.get_new_entries()
    ]

class ContractWatcher:

    def __init__(self, web3, ipfs, contract):
        self.web3 = web3
        self.ipfs = ipfs
        self.contract = contract

    def log_loop(self, event_filters, interval=5):
        while True:
            for event in getAllEvents(event_filters):
                LOG.info('Event: %s', event['event'])
                pack_chash = ipfsBinToText(event['args']['contenthash'].hex())
                pack = StickerPack(pack_chash)
                pack.pin(self.ipfs)

            LOG.debug('Sleeping for: %ss', interval)
            time.sleep(interval)

    def loop(self, event_names, interval=5):
        filters = [
            getattr(
                self.contract.contract.events, event_name
            ).createFilter(fromBlock=self.web3.eth.blockNumber)
            for event_name in event_names
        ]
        self.log_loop(filters, interval)
