#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import time
import os
import sys

# ─── BANNER ────────────────────────────────────────────────
BANNER = r"""
  ███╗   ██╗███████╗██╗  ██╗      ██████╗██████╗  █████╗  ██████╗██╗  ██╗
  ████╗  ██║██╔════╝╚██╗██╔╝     ██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
  ██╔██╗ ██║█████╗   ╚███╔╝      ██║     ██████╔╝███████║██║     █████╔╝
  ██║╚██╗██║██╔══╝   ██╔██╗      ██║     ██╔══██╗██╔══██║██║     ██╔═██╗
  ██║ ╚████║███████╗██╔╝ ██╗     ╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝

    Version : 2.3
    Creator : Ahmad Bilal Qureshi
    TikTok  : @nexreaper_69
    Insta   : @dex7er_0
    Phone   : +923005381443
"""

# ─── UTILITY FUNCTIONS ─────────────────────────────────────

def get_hash_function(algo):
    """Return the appropriate hashlib function for the given algorithm."""
    algo = algo.upper()
    if algo == "MD5":
        return hashlib.md5
    elif algo == "SHA1":
        return hashlib.sha1
    elif algo == "SHA256":
        return hashlib.sha256
    elif algo == "SHA512":
        return hashlib.sha512
    else:
        return None

def compute_hash(data, algo):
    """Compute hash of data (bytes) using the specified algorithm."""
    h = get_hash_function(algo)
    if h is None:
        return None
    return h(data).hexdigest()

# ─── CRACKING ENGINE ───────────────────────────────────────

# A small list of common passwords to try first (optional)
COMMON_PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "abc123", "password123",
    "admin", "letmein", "welcome", "monkey", "dragon", "master",
    "football", "baseball", "iloveyou", "sunshine", "princess", "123123"
]

def crack_hash(wordlist_path, hash_algo, target_hash):
    """
    Cracks the target hash by reading the wordlist line by line.
    Returns (found_password, attempts, elapsed_time) or (None, attempts, elapsed_time).
    """
    # Validate hash algorithm
    h_func = get_hash_function(hash_algo)
    if h_func is None:
        print(f"[-] Unsupported hash type: {hash_algo}")
        return None, 0, 0.0

    # Check if wordlist exists
    if not os.path.isfile(wordlist_path):
        print(f"[-] Wordlist file not found: {wordlist_path}")
        return None, 0, 0.0

    # Normalize target hash (lowercase)
    target_hash = target_hash.strip().lower()

    # Try common passwords first (if the list is provided)
    print("[*] Trying common passwords first...")
    for pwd in COMMON_PASSWORDS:
        computed = h_func(pwd.encode('utf-8')).hexdigest()
        if computed == target_hash:
            return pwd, 1, 0.0   # time not measured for these

    # Now stream the wordlist
    print(f"[*] Streaming wordlist: {wordlist_path}")
    attempts = len(COMMON_PASSWORDS)
    start_time = time.time()
    last_progress = 0
    found = None

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                pwd = line.rstrip('\n\r')
                if not pwd:
                    continue
                attempts += 1
                computed = h_func(pwd.encode('utf-8')).hexdigest()
                if computed == target_hash:
                    found = pwd
                    break

                # Progress every 50,000 lines
                if attempts % 50000 == 0:
                    elapsed = time.time() - start_time
                    speed = attempts / elapsed if elapsed > 0 else 0
                    print(f"[*] Progress: {attempts:,} lines tested, "
                          f"speed: {speed:.0f} h/s, elapsed: {elapsed:.1f}s")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        return None, attempts, time.time() - start_time
    except Exception as e:
        print(f"[-] Error reading wordlist: {e}")
        return None, attempts, time.time() - start_time

    elapsed = time.time() - start_time
    return found, attempts, elapsed

# ─── MENU OPTIONS ──────────────────────────────────────────

def menu_crack_hash():
    print("\n=== Crack Hash (Wordlist Only) ===")
    wordlist = input("Enter full wordlist path (default: rockyou.txt): ").strip()
    if not wordlist:
        wordlist = "rockyou.txt"
        print(f"Using default: {wordlist}")

    print("Choose hash type: MD5, SHA1, SHA256, SHA512")
    algo = input("Hash type: ").strip().upper()
    if algo not in ("MD5", "SHA1", "SHA256", "SHA512"):
        print("[-] Invalid hash type.")
        return

    target = input("Enter the hash value: ").strip()
    if not target:
        print("[-] No hash provided.")
        return

    print(f"[*] Starting crack for {algo} hash: {target}")
    found, attempts, elapsed = crack_hash(wordlist, algo, target)

    if found:
        print(f"\n[+] CRACKED!")
        print(f"    Password : {found}")
        print(f"    Attempts : {attempts:,}")
        print(f"    Time     : {elapsed:.2f} seconds")
    else:
        print(f"\n[-] Hash not found in wordlist.")
        print(f"    Attempts : {attempts:,}")
        print(f"    Time     : {elapsed:.2f} seconds")

def menu_decrypt_hex():
    print("\n=== Decrypt Hex String ===")
    hex_str = input("Enter hex string: ").strip()
    if not hex_str:
        print("[-] No input.")
        return
    try:
        # Remove spaces if any
        hex_str = hex_str.replace(" ", "")
        decoded = bytes.fromhex(hex_str).decode('utf-8', errors='replace')
        print(f"[+] Decrypted text: {decoded}")
    except ValueError:
        print("[-] Invalid hex string.")

def menu_generate_hashes():
    print("\n=== Generate Hashes (MD5/SHA) ===")
    text = input("Enter text to hash: ").strip()
    if not text:
        print("[-] No text.")
        return

    data = text.encode('utf-8')
    print("\n[+] Hashes:")
    print(f"MD5    : {hashlib.md5(data).hexdigest()}")
    print(f"SHA1   : {hashlib.sha1(data).hexdigest()}")
    print(f"SHA256 : {hashlib.sha256(data).hexdigest()}")
    print(f"SHA512 : {hashlib.sha512(data).hexdigest()}")

def menu_add_word():
    print("\n=== Add to Wordlist ===")
    wordlist = input("Enter path to wordlist (default: rockyou.txt): ").strip()
    if not wordlist:
        wordlist = "rockyou.txt"
    new_word = input("Enter word to add: ").strip()
    if not new_word:
        print("[-] No word.")
        return
    try:
        with open(wordlist, 'a', encoding='utf-8') as f:
            f.write(new_word + '\n')
        print(f"[+] Word '{new_word}' added to {wordlist}")
    except Exception as e:
        print(f"[-] Error: {e}")

def menu_exit():
    print("\n[+] Exiting Nex-Crack. Goodbye!")
    sys.exit(0)

# ─── MAIN ──────────────────────────────────────────────────

def main():
    # Clear screen (optional)
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

    while True:
        print("\n" + "=" * 50)
        print(" MAIN MENU")
        print("=" * 50)
        print("1. Crack Hash (Wordlist Only)")
        print("2. Decrypt Hex String")
        print("3. Generate Hashes (MD5/SHA)")
        print("4. Add to wordlist")
        print("5. Exit")
        print("=" * 50)

        choice = input("Select an option: ").strip()
        if choice == "1":
            menu_crack_hash()
        elif choice == "2":
            menu_decrypt_hex()
        elif choice == "3":
            menu_generate_hashes()
        elif choice == "4":
            menu_add_word()
        elif choice == "5":
            menu_exit()
        else:
            print("[-] Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted. Exiting...")
        sys.exit(0)
