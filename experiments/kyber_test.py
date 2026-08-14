import oqs

print("Available KEM algorithms:")
print(oqs.get_enabled_kem_mechanisms())

print("\nRunning Kyber512...\n")

# Initialize Kyber
kem = oqs.KeyEncapsulation("Kyber512")

# Bob generates keypair
public_key = kem.generate_keypair()
private_key = kem.export_secret_key()

print("Public key generated")

# Alice creates ciphertext and shared secret
ciphertext, shared_secret_alice = kem.encap_secret(public_key)

print("Ciphertext created")

# Bob reconstructs shared secret
shared_secret_bob = kem.decap_secret(ciphertext)

print("Shared secret (Alice):", shared_secret_alice[:10], "...")
print("Shared secret (Bob):", shared_secret_bob[:10], "...")

# Verify
if shared_secret_alice == shared_secret_bob:
    print("\nShared secrets match!")
else:
    print("\nError: mismatch")
