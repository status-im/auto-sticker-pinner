import time

class ContractWatcher:

    def __init__(self, web3, contract):
        self.web3 = web3
        self.contract = contract

    def handle_event(self, event):
        print(event)

    def log_loop(self, event_filter, poll_interval=1):
        while True:
            for event in event_filter.get_new_entries():
                handle_event(event)
            time.sleep(poll_interval)

    def loop(self, event_name):
        event = getattr(self.contract.contract.events, event_name)
        evFilter = event.createFilter(fromBlock=self.web3.eth.blockNumber)
        self.log_loop(evFilter, 2)
