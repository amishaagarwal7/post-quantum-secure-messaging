import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os

# Step 1: Bob generates keypair
kem = oqs.KeyEncapsulation("Kyber512")
public_key = kem.generate_keypair()
secret_key = kem.export_secret_key()

# Step 2: Alice encapsulates
ciphertext_kem, shared_secret_alice = kem.encap_secret(public_key)

# Step 3: Bob decapsulates
shared_secret_bob = kem.decap_secret(ciphertext_kem)

# Step 4: Derive AES key
aes_key_alice = hashlib.sha256(shared_secret_alice).digest()
aes_key_bob = hashlib.sha256(shared_secret_bob).digest()

# Step 5: AES encryption (Alice)
aesgcm = AESGCM(aes_key_alice)
nonce = os.urandom(12)

message = b"Hello Bob, secure message"
ciphertext = aesgcm.encrypt(nonce, message, None)

# Step 6: AES decryption (Bob)
aesgcm_bob = AESGCM(aes_key_bob)
decrypted = aesgcm_bob.decrypt(nonce, ciphertext, None)

print("Decrypted:", decrypted)
