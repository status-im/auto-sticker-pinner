class StickerPackContract:

    def __init__(self, contract_address, contract_abi, w3):
        self.address = contract_address
        self.abi = contract_abi
        self.w3 = w3
        # Create an instance of web3.py contract
        self.contract = w3.eth.contract(
            address=self.address,
            abi=self.abi
        )

    def getAllPacks(self):
        return self.contract.functions.totalSupply().call()
        #for i=0; i<stickerTypeContract stickerTypeContract.functions.getPackSummary(i)
