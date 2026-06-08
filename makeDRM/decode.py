import os
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def prepare_bytes(text: str, size: int) -> bytes:
    b = text.encode("utf-8")
    return b + b"\x00" * (size - len(b)) if len(b) < size else b[:size]


def decode_file(input_path: str, output_path: str | None = None) -> str:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_path}")

    with open(input_path, "rb") as f:
        encrypted_bytes = f.read()

    key = prepare_bytes("PassNote", 32)
    iv = prepare_bytes("newlearn", 16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(encrypted_bytes)

    try:
        decrypted_bytes = unpad(decrypted_padded, AES.block_size)
    except ValueError as e:
        raise ValueError(
            "복호화는 되었지만 unpad에 실패했습니다. "
            "키/IV가 다르거나 입력 파일이 암호화된 PDF가 아닐 수 있습니다."
        ) from e

    if output_path is None:
        base, ext = os.path.splitext(input_path)
        if ext.lower() == ".pdf":
            output_path = f"{base}_decoded.pdf"
        else:
            output_path = f"{input_path}_decoded.pdf"

    with open(output_path, "wb") as f:
        f.write(decrypted_bytes)

    return output_path


def main():
    parser = argparse.ArgumentParser(description="PassNote AES-CBC PDF decode script")
    parser.add_argument("--input", required=True, help="암호화된 입력 파일 경로")
    parser.add_argument("--output", help="복호화된 PDF 저장 경로 (선택)")
    args = parser.parse_args()

    try:
        output_path = decode_file(args.input, args.output)
        print(f"복호화 완료: {output_path}")
    except Exception as e:
        print(f"에러: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()