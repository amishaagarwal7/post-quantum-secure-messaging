import oqs

users = {}

def create_user(name):
    kem = oqs.KeyEncapsulation("Kyber512")
    public_key = kem.generate_keypair()
    secret_key = kem.export_secret_key()
    
    sig = oqs.Signature("ML-DSA-44")
    public_key_sig = sig.generate_keypair()
    secret_key_sig = sig.export_secret_key()

    users[name] = {
        "kem": kem,
        "public_key": public_key,
        "secret_key": secret_key,
        
        "sig": sig,
        "sig_public_key": public_key_sig,
        "sig_secret_key": secret_key_sig
    }

#print(users)
sessions= {}
def establish_session(sender, receiver):

    receiver_data = users[receiver]

    kem = receiver_data["kem"]
    public_key = receiver_data["public_key"]

    ciphertext, shared_secret = kem.encap_secret(public_key)

    shared_secret_receiver = kem.decap_secret(ciphertext)

    import hashlib
    key = hashlib.sha256(shared_secret).digest()

    sessions[(sender, receiver)] = key
    sessions[(receiver, sender)] = key

    print(f"Session created between {sender} and {receiver}")

#establish_session("Alice", "Bob")
#print(sessions)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def send_message(sender, receiver, message):

    # Step 1: check session
    if (sender, receiver) not in sessions:
        establish_session(sender, receiver)

    key = sessions[(sender, receiver)]

    # Step 2: AES encrypt
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    
    sender_data = users[sender]
    sig = sender_data["sig"]
    signature = sig.sign(message.encode())
    ciphertext = aesgcm.encrypt(nonce, message.encode(), None)

    print(f"\n{sender} → {receiver}")
    print("Encrypted:", ciphertext)

    # Step 3: send to receiver
    result=receive_message(receiver, sender, nonce, ciphertext,signature)
    return result


def receive_message(receiver, sender, nonce, ciphertext,signature):

    key = sessions[(receiver, sender)]

    aesgcm = AESGCM(key)

    from cryptography.exceptions import InvalidTag

    try:
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        print("Decryption failed: message was tampered")
        return

    # --- ADD VERIFICATION HERE ---
    sender_data = users[sender]

    sig = sender_data["sig"]
    public_key = sender_data["sig_public_key"]

    is_valid = sig.verify(decrypted, signature, public_key)

    if is_valid:
        print("Signature verified: message is authentic")
        return decrypted.decode(), is_valid
    
    else:
        print("Signature verification FAILED: message may be tampered")

#send_message("Alice", "Bob", "Hello Bob")
#send_message("Alice", "Bob", "Second message")

#if __name__ == "__main__":
    #create_user("Alice")
    #create_user("Bob")

    #send_message("Alice", "Bob", "Hello Bob")
    #send_message("Alice", "Bob", "Second message")
    
    

