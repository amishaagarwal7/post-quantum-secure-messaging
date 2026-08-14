from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import hashlib

# Temporary shared secret (for testing)
shared_secret = b"this_is_test_shared_secret"

aes_key = hashlib.sha256(shared_secret).digest()

print(len(aes_key))
aesgcm = AESGCM(aes_key)
nonce = os.urandom(12)
print("Nonce:", nonce)
print("Nonce length:", len(nonce))

message = b"Hello Bob, this is Alice"

# Step 6: encrypt
ciphertext = aesgcm.encrypt(nonce, message, None)
print("Ciphertext:", ciphertext)

# Step 7: decrypt
decrypted = aesgcm.decrypt(nonce, ciphertext, None)
print("Decrypted:", decrypted)

# Step 8: tamper test
tampered = bytearray(ciphertext)
tampered[0] ^= 1

aesgcm.decrypt(nonce, bytes(tampered), None)
