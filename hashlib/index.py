import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, data, difficulty=4):
        self.index = index
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()

    def calculate_hash(self):
        # Blok verilerini birleştirip SHA-256 hash'ini hesaplar
        value = f"{self.index}{self.timestamp}{self.previous_hash}{self.data}{self.nonce}"
        return hashlib.sha256(value.encode('utf-8')).hexdigest()

    def mine_block(self):
        # Belirlenen zorluk derecesi kadar sıfır ile başlayan hash arar
        target = "0" * self.difficulty
        while True:
            current_hash = self.calculate_hash()
            if current_hash.startswith(target):
                print(f"Blok #{self.index} kazıldı! Nonce: {self.nonce} | Hash: {current_hash}")
                return current_hash
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Zincirin ilk (Genesis) bloğu
        return Block(0, "0", "Genesis Blok", self.difficulty)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), latest_block.hash, data, self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Zincirin bütünlüğünü kontrol eder
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# --- Kullanım Örneği ---
if __name__ == "__main__":
    print("Blok zinciri oluşturuluyor...\n")
    my_coin = Blockchain(difficulty=4)

    print("\nYeni bloklar ekleniyor...")
    my_coin.add_block("Transfer: Alice -> Bob (10 BTC)")
    my_coin.add_block("Transfer: Bob -> Charlie (5 BTC)")

    print(f"\nZincir geçerli mi? {my_coin.is_chain_valid()}")
