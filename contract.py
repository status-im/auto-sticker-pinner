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
        count = self.contract.functions.totalSupply().call()
        return [
            self.contentHashFromPack(
                self.contract.functions.getPackSummary(i).call()
            ) for i in range(count)
        ]

    @staticmethod
    def contentHashFromPack(pack):
        return pack[2].hex()
