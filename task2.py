from PIL import Image
import numpy as np
import os

def load_image(image_path):
    """Load an image from a file path and convert it to a numpy array."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file '{image_path}' does not exist.")
    
    img = Image.open(image_path)
    img_array = np.array(img)
    
    if img_array.ndim != 3:
        raise ValueError("Only RGB images are supported.")
    
    return img_array

def save_image(img_array, output_path):
    """Save a numpy array as an image to a specified path."""
    img = Image.fromarray(img_array.astype('uint8'))
    img.save(output_path)
    print(f"Image saved as '{output_path}'")

def encrypt_image(image_path, key, operation='add'):
    """
    Encrypt an image by modifying pixel values using a specified key and operation.
    
    Supported operations: 'add', 'subtract', 'xor', 'swap'
    """
    img_array = load_image(image_path)
    
    if operation == 'add':
        print("Encrypting with addition...")
        encrypted_array = (img_array + key) % 256
    elif operation == 'subtract':
        print("Encrypting with subtraction...")
        encrypted_array = (img_array - key) % 256
    elif operation == 'xor':
        print("Encrypting with XOR...")
        encrypted_array = img_array ^ key
    elif operation == 'swap':
        print("Encrypting by swapping pixels...")
        encrypted_array = swap_pixels(img_array, key)
    else:
        raise ValueError("Unsupported operation. Choose 'add', 'subtract', 'xor', or 'swap'.")
    
    save_image(encrypted_array, 'encrypted_image.png')
    print("Encryption complete.")

def decrypt_image(image_path, key, operation='add'):
    """
    Decrypt an image by reversing the encryption process using the same key and operation.
    
    Supported operations: 'add', 'subtract', 'xor', 'swap'
    """
    img_array = load_image(image_path)
    
    if operation == 'add':
        print("Decrypting with subtraction...")
        decrypted_array = (img_array - key) % 256
    elif operation == 'subtract':
        print("Decrypting with addition...")
        decrypted_array = (img_array + key) % 256
    elif operation == 'xor':
        print("Decrypting with XOR...")
        decrypted_array = img_array ^ key
    elif operation == 'swap':
        print("Decrypting by swapping pixels...")
        decrypted_array = swap_pixels(img_array, key)
    else:
        raise ValueError("Unsupported operation. Choose 'add', 'subtract', 'xor', or 'swap'.")
    
    save_image(decrypted_array, 'decrypted_image.png')
    print("Decryption complete.")

def swap_pixels(img_array, key):
    """
    Swap pixel values based on a key. This swaps pixels in pairs, determined by the key.
    """
    img_shape = img_array.shape
    flat_img = img_array.flatten()
    np.random.seed(key)  # Ensure swaps are reproducible with the same key
    
    indices = np.arange(len(flat_img))
    np.random.shuffle(indices)  # Shuffle indices for swapping
    
    swapped_img = np.empty_like(flat_img)
    
    # Swap pairs of pixels
    for i in range(0, len(indices), 2):
        if i + 1 < len(indices):
            swapped_img[indices[i]] = flat_img[indices[i+1]]
            swapped_img[indices[i+1]] = flat_img[indices[i]]
        else:
            swapped_img[indices[i]] = flat_img[indices[i]]  # Leave the last pixel unswapped if odd length
    
    return swapped_img.reshape(img_shape)

def get_user_input():
    """
    Get user input for the image path, key, operation, and whether to encrypt or decrypt.
    """
    image_path = input("Enter the path of the image file: ")
    key = int(input("Enter the encryption key (integer): "))
    operation = input("Enter the operation ('add', 'subtract', 'xor', 'swap'): ").lower()
    mode = input("Enter mode ('encrypt' or 'decrypt'): ").lower()
    
    return image_path, key, operation, mode

def main():
    """Main function to run the encryption or decryption based on user input."""
    try:
        image_path, key, operation, mode = get_user_input()
        
        if mode == 'encrypt':
            encrypt_image(image_path, key, operation)
        elif mode == 'decrypt':
            decrypt_image(image_path, key, operation)
        else:
            print("Invalid mode. Please enter 'encrypt' or 'decrypt'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
