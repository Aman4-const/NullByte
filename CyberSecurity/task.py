def caesar_cipher(text, shift, mode):
    result = ""
    
    for char in text:
        if char.isalpha():
            # Convert to lowercase or uppercase depending on char
            base = ord('A') if char.isupper() else ord('a')
            
            # Apply the Caesar shift
            if mode == "encrypt":
                result += chr((ord(char) - base + shift) % 26 + base)
            elif mode == "decrypt":
                result += chr((ord(char) - base - shift) % 26 + base)
        else:
            # Keep punctuation, numbers, and spaces unchanged
            result += char
    
    return result


def main():
    print("=== Caesar Cipher Encryption/Decryption ===")
    message = input("Enter your message: ")
    while True:
        try:
            shift = int(input("Enter shift value (integer): "))
            break
        except ValueError:
            print("Please enter a valid number.")
    
    mode = ""
    while mode not in ["encrypt", "decrypt"]:
        mode = input("Type 'encrypt' to encrypt or 'decrypt' to decrypt: ").lower()

    result = caesar_cipher(message, shift, mode)
    print(f"\nResult ({mode}ed message): {result}")


if __name__ == "__main__":
    main()
