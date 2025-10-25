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

# --- Logika Client ---

def receive_messages(client_socket):
    """Fungsi untuk menerima pesan dari server"""
    while True:
        try:
            encrypted_message = client_socket.recv(1024).decode('utf-8')
            if not encrypted_message:
                print("Koneksi server terputus.")
                break
            
            decrypted_message = decrypt_message(encrypted_message, KEY)
            # Menampilkan pesan yang sudah didekripsi
            print(f"\rServer: {decrypted_message}\nAnda > ", end="")
        except:
            print("Koneksi terputus.")
            break
    client_socket.close()

def send_messages(client_socket):
    """Fungsi untuk mengirim pesan ke server"""
    while True:
        try:
            message = input("Anda > ")
            encrypted_message = encrypt_message(message, KEY)
            
            # Menampilkan ciphertext sebelum dikirim
            print(f"(Mengirim ciphertext: {encrypted_message})")
            
            client_socket.send(encrypted_message.encode('utf-8'))
        except:
            print("Gagal mengirim pesan. Koneksi mungkin terputus.")
            break
    client_socket.close()

def start_client():
    server_ip = input("Masukkan IP Address Server: ")
    port = 1010

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print(f"Berhasil terhubung ke server di {server_ip}:{port}. Selamat mengobrol!")
    except socket.error as e:
        print(f"Gagal terhubung ke server: {e}")
        return

    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    send_thread = threading.Thread(target=send_messages, args=(client,))
    
    recv_thread.start()
    send_thread.start()
    
    recv_thread.join()
    send_thread.join()
    
    print("Sesi chat berakhir.")
    client.close()

if __name__ == "__main__":
    start_client()