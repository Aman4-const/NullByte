from __future__ import annotations

import argparse
import random
from typing import List, Sequence, Tuple

from PIL import Image


# ---------------------------- Utility functions ---------------------------- #

def _ensure_rgba(img: Image.Image) -> Image.Image:
    """Convert image to RGBA so we can handle all modes consistently."""
    if img.mode != "RGBA":
        return img.convert("RGBA")
    return img


def _apply_pixel_op_to_rgb(pixel: Tuple[int, int, int, int], op: str | None, key: int | None) -> Tuple[int, int, int, int]:
    r, g, b, a = pixel
    if op is None or key is None:
        return (r, g, b, a)

    if op == "xor":
        r2 = r ^ key
        g2 = g ^ key
        b2 = b ^ key
    elif op == "add":
        r2 = (r + key) % 256
        g2 = (g + key) % 256
        b2 = (b + key) % 256
    elif op == "sub":
        r2 = (r - key) % 256
        g2 = (g - key) % 256
        b2 = (b - key) % 256
    else:
        raise ValueError(f"Unsupported op: {op}")

    return (r2, g2, b2, a)


def _inverse_op(op: str | None) -> str | None:
    if op is None:
        return None
    if op == "xor":
        return "xor"  # self-inverse
    if op == "add":
        return "sub"
    if op == "sub":
        return "add"
    raise ValueError(f"Unsupported op: {op}")


def _shuffle_indices(n: int, seed: int) -> List[int]:
    """Return a deterministic permutation of range(n)."""
    idx = list(range(n))
    rng = random.Random(seed)
    rng.shuffle(idx)
    return idx


def _invert_permutation(p: Sequence[int]) -> List[int]:
    inv = [0] * len(p)
    for i, pi in enumerate(p):
        inv[pi] = i
    return inv


# ---------------------------- Core transforms ----------------------------- #

def encrypt_image(img: Image.Image, op: str | None, key: int | None, shuffle_seed: int | None) -> Image.Image:
    """Apply (1) per‑pixel op then (2) index shuffle."""
    img = _ensure_rgba(img)
    pixels = list(img.getdata())

    # 1) per‑pixel op on RGB
    if op is not None and key is None:
        raise ValueError("--key is required when --op is provided")

    if op is not None:
        pixels = [_apply_pixel_op_to_rgb(px, op, key) for px in pixels]

    # 2) pixel shuffle
    if shuffle_seed is not None:
        perm = _shuffle_indices(len(pixels), shuffle_seed)
        shuffled = [None] * len(pixels)
        for i, pi in enumerate(perm):
            shuffled[i] = pixels[pi]
        pixels = shuffled

    out = Image.new("RGBA", img.size)
    out.putdata(pixels)
    return out


def decrypt_image(img: Image.Image, op: str | None, key: int | None, shuffle_seed: int | None) -> Image.Image:
    """Inverse of encrypt: (1) unshuffle then (2) inverse per‑pixel op."""
    img = _ensure_rgba(img)
    pixels = list(img.getdata())

    # 1) unshuffle (inverse permutation)
    if shuffle_seed is not None:
        perm = _shuffle_indices(len(pixels), shuffle_seed)
        inv = _invert_permutation(perm)
        unshuffled = [None] * len(pixels)
        for i, inv_i in enumerate(inv):
            unshuffled[i] = pixels[inv_i]
        pixels = unshuffled

    # 2) inverse per‑pixel op
    if op is not None and key is None:
        raise ValueError("--key is required when --op is provided")

    inv_op = _inverse_op(op)
    if inv_op is not None:
        pixels = [_apply_pixel_op_to_rgb(px, inv_op, key) for px in pixels]

    out = Image.new("RGBA", img.size)
    out.putdata(pixels)
    return out


# ------------------------------ CLI handling ------------------------------ #

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Simple image obfuscation via pixel manipulation (NOT secure)")
    sub = p.add_subparsers(dest="command", required=True)

    def add_common(sp: argparse.ArgumentParser):
        sp.add_argument("input", help="Input image path")
        sp.add_argument("output", help="Output image path")
        sp.add_argument("--op", choices=["xor", "add", "sub"], help="Per‑pixel operation to apply to RGB channels")
        sp.add_argument("--key", type=int, help="Integer key (0–255 recommended)")
        sp.add_argument("--shuffle-seed", type=int, help="Deterministic shuffle seed (enables pixel shuffling)")

    add_common(sub.add_parser("encrypt", help="Encrypt/obfuscate image"))
    add_common(sub.add_parser("decrypt", help="Decrypt/de‑obfuscate image"))

    return p.parse_args()


def main():
    args = parse_args()

    img = Image.open(args.input)

    if args.command == "encrypt":
        out = encrypt_image(img, args.op, args.key, args.shuffle_seed)
    elif args.command == "decrypt":
        out = decrypt_image(img, args.op, args.key, args.shuffle_seed)
    else:
        raise RuntimeError("Unknown command")

    # Preserve original format from output extension
    out.save(args.output)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()