import socket
import threading

# --- Logika Kriptografi Caesar Cipher ---
# Kunci (key) = 3,
KEY = 3

def encrypt_message(plaintext, key):
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            encrypted_char_code = (ord(char) - start + key) % 26
            ciphertext += chr(start + encrypted_char_code)
        else:
            ciphertext += char
    return ciphertext

def decrypt_message(ciphertext, key):
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            decrypted_char_code = (ord(char) - start - key) % 26
            plaintext += chr(start + decrypted_char_code)
        else:
            plaintext += char
    return plaintext

# --- Logika Server ---

def receive_messages(client_socket):
    """Fungsi untuk menerima pesan dari klien"""
    while True:
        try:
            encrypted_message = client_socket.recv(1024).decode('utf-8')
            if not encrypted_message:
                print("Koneksi klien terputus.")
                break
            
            decrypted_message = decrypt_message(encrypted_message, KEY)
            
            print(f"\r[Ciphertext Diterima]: {encrypted_message}")
            
            print(f"Klien: {decrypted_message}\nAnda > ", end="")
            
        except:
            print("Koneksi terputus.")
            break
    client_socket.close()

def send_messages(client_socket):
    """Fungsi untuk mengirim pesan ke klien"""
    while True:
        try:
            message = input("Anda > ")
            encrypted_message = encrypt_message(message, KEY)
            
            print(f"(Mengirim ciphertext: {encrypted_message})")
            
            client_socket.send(encrypted_message.encode('utf-8'))
        except:
            print("Gagal mengirim pesan. Koneksi mungkin terputus.")
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1010)) 
    server.listen(1)
    print("[SERVER DIMULAI] Menunggu 1 koneksi klien...")

    client_socket, addr = server.accept()
    print(f"[KLIEN TERHUBUNG] dari {addr}. Selamat mengobrol!")

    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    
    recv_thread.start()
    send_thread.start()
    
    recv_thread.join()
    send_thread.join()
    
    print("Sesi chat berakhir.")
    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()