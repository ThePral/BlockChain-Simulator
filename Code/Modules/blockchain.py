from Code.Modules.block import Block
from Code.Modules.transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
        self.pending_transactions = []
        self.mining_reward = 50

    def create_genesis_block(self):
        return Block(index=0, transactions="Genesis Block", previous_hash="0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.from_address or not transaction.to_address:
            raise ValueError("Transaction must include from and to address")

        if not transaction.is_valid():
            raise ValueError("Invalid transaction: signature check failed")

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        reward_tx = Transaction(from_address="System", to_address=miner_address, amount=self.mining_reward)

        self.pending_transactions.append(reward_tx)

        new_block = Block(
            index=len(self.chain),
            transactions=[tx.__dict__ for tx in self.pending_transactions],
            previous_hash=self.get_latest_block().hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print("Block hash mismatch")
                return False

            if current.previous_hash != previous.hash:
                print("Previous hash mismatch")
                return False

            if isinstance(current.transactions, list):
                for tx_data in current.transactions:
                    if tx_data['from_address'] == 'System':
                        continue
                    tx = Transaction(
                        from_address=tx_data['from_address'],
                        to_address=tx_data['to_address'],
                        amount=tx_data['amount']
                    )
                    tx.signature = tx_data['signature']
                    if not tx.is_valid():
                        print("Invalid transaction signature in block", i)
                        return False

        return True

    def get_balance_of_address(self, address, balance):
        # balance = 0
        for block in self.chain:
            if isinstance(block.transactions, list):
                for tx in block.transactions:
                    if tx['from_address'] == address:
                        balance -= tx['amount']
                    if tx['to_address'] == address:
                        balance += tx['amount']
        return balance
