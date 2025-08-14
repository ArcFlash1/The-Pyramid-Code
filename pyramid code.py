# pyramid_cipher_poly.py
"""
Pyramid Cipher (Triangle Traversal) — Mono & Polyalphabetic
Author: Arc Flash
Date: 14/08/2025

Traversal order (rightward encoding path):
Q J E B A D I P Y R K F C H O X S L G N W T M V U
Z is outside the triangle and maps to itself (Z -> Z).

Features:
- Monoalphabetic: move 1 step right (encode) or left (decode).
- Polyalphabetic: move n steps per character using a numeric key sequence (e.g., 1,2,3).
- Preserves case and non-letters.
"""

from typing import Iterable, List
import argparse


ORDER = "QJEBADIPYRKFCHOXSLGNWTMVU"
ORDER_SET = set(ORDER)

def _normalize_key(key: Iterable[int] | None) -> List[int] | None:
    if key is None:
        return None
    k = [int(x) for x in key]
    if not k:
        return None
    # Reduce huge steps modulo path length (keeps behavior intuitive)
    return [n % len(ORDER) for n in k]

def _shift_char(ch: str, steps: int, encode: bool) -> str:
    # Non-letters pass through unchanged
    if not ch.isalpha():
        return ch

    # Z/z maps to itself
    if ch.upper() == "Z":
        return ch

    upper = ch.upper()
    if upper not in ORDER_SET:
        # If someone extends alphabet, just pass through
        return ch

    idx = ORDER.index(upper)
    delta = steps % len(ORDER)
    new_idx = (idx + (delta if encode else -delta)) % len(ORDER)
    out = ORDER[new_idx]
    return out if ch.isupper() else out.lower()

def encode(text: str, key: Iterable[int] | None = None) -> str:
    k = _normalize_key(key)
    if k is None:
        k = [1]  # mono default
    out = []
    ki = 0
    for ch in text:
        out.append(_shift_char(ch, k[ki], encode=True))
        if ch.isalpha():
            ki = (ki + 1) % len(k)
    return "".join(out)

def decode(text: str, key: Iterable[int] | None = None) -> str:
    k = _normalize_key(key)
    if k is None:
        k = [1]  # mono default
    out = []
    ki = 0
    for ch in text:
        out.append(_shift_char(ch, k[ki], encode=False))
        if ch.isalpha():
            ki = (ki + 1) % len(k)
    return "".join(out)

def main():
    p = argparse.ArgumentParser(description="Pyramid (Triangle) Cipher")
    p.add_argument("message", nargs="?", help="Text to encode/decode. If omitted, prompts interactively.")
    p.add_argument("-m", "--mode", choices=["e","d"], help="e=encode, d=decode")
    p.add_argument("-k", "--key", help="Numeric key sequence (comma-separated), e.g. 2,1,3")
    args = p.parse_args()

    if args.message is None or args.mode is None:
        # Interactive fallback
        msg = input("Enter message: ")
        mode = input("Encode or Decode (e/d)? ").strip().lower()
        key_str = input("Key (comma numbers) or blank for mono: ").strip()
    else:
        msg = args.message
        mode = args.mode
        key_str = args.key or ""

    key = None
    if key_str:
        key = [int(x.strip()) for x in key_str.split(",") if x.strip()]

    if mode == "e":
        print(encode(msg, key))
    elif mode == "d":
        print(decode(msg, key))
    else:
        print("Invalid mode. Use e or d.")

if __name__ == "__main__":
    main()

