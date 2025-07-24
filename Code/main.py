from Modules.wallet import Wallet
from Modules.blockchain import Blockchain

# 1. Create wallets for Ali, Reza, and the Miner
ali = Wallet()
reza = Wallet()
miner = Wallet()

print("✅ Wallets Created")
print("\nAli Public Key:", ali.get_public_key_hex())
print("\nReza Public Key:", reza.get_public_key_hex())
print("\nMiner Public Key:", miner.get_public_key_hex())

# 2. Create a new blockchain
my_chain = Blockchain()
print("\n✅ Blockchain Initialized")

# 3. Ali sends 25 coins to Reza
tx1 = ali.create_signed_transaction(to_address=reza.get_public_key_hex(), amount=25)

# 4. Add transaction to blockchain
my_chain.add_transaction(tx1)
print("\n🧾 Transaction added (Ali → Reza)")

# 5. Miner mines the block
print("\n⛏️  Mining pending transactions...")
my_chain.mine_pending_transactions(miner_address=miner.get_public_key_hex())

# 6. Display balances
print("\n💰 Balances after mining:")
print("Ali:", my_chain.get_balance_of_address(ali.get_public_key_hex(), 55))
print("Reza:", my_chain.get_balance_of_address(reza.get_public_key_hex(), 10))
print("Miner:", my_chain.get_balance_of_address(miner.get_public_key_hex(), 0))

# 7. Chain validation
print("\n🔍 Chain is valid?", my_chain.is_chain_valid())
