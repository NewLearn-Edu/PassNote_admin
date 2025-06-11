import os
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import zipfile
import random
import fitz  # PyMuPDF
import sys
import threading
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import io
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

 
sys.setrecursionlimit(sys.getrecursionlimit() * 5)


def encrypt_pdfs():
    start_time = time.time()
    try:
        # Select the folder containing PDF files
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        # List all PDF files in the folder
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

        if not pdf_files:
            messagebox.showwarning("경고", "선택한 폴더에 PDF 파일이 없습니다.")
            return

        progress["maximum"] = len(pdf_files)
        progress_status.config(text=f"0 / {len(pdf_files)} 완료됨")

        # Create a DataFrame with required columns
        columns = ["Name", "Description", "Author", "Publisher", "PublicationDate", "Price", "Pages", "ISBN"]

        # Save path is set to folder_path (where PDFs are located)
        save_path = os.path.join(os.path.dirname(folder_path), "passNote_Upload")
        os.makedirs(save_path, exist_ok=True)
        log("EXCEL 파일 생성 완료")

        log("암호화 시작")

        def process_pdf_file(pdf_file):
            name_without_ext = os.path.splitext(pdf_file)[0]
            full_pdf_path = os.path.join(folder_path, pdf_file)

            # 1. Read PDF
            log(f"{pdf_file}파일 읽는 중")
            reader = PdfReader(full_pdf_path)
            writer_full = PdfWriter()
            for page in reader.pages:
                writer_full.add_page(page)

            # 2. Save first page as image using PyMuPDF
            log(f"{pdf_file} 썸네일 생성 중")
            doc = fitz.open(full_pdf_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            jpg_path = os.path.join(save_path, f"{name_without_ext}.jpg")
            pix.save(jpg_path)
            doc.close()

            # 3. Create preview PDF with 10% random pages
            log(f"{pdf_file} 미리보기 생성중")
            num_pages = len(reader.pages)

            row = [name_without_ext, "", "", "", "", "", num_pages, ""]

            num_preview_pages = max(1, int(num_pages * 0.1))
            sampled_indices = sorted(random.sample(range(num_pages), num_preview_pages))
            writer_preview = PdfWriter()
            for idx in sampled_indices:
                writer_preview.add_page(reader.pages[idx])
            preview_path = os.path.join(save_path, f"{name_without_ext}_preview.pdf")
            with open(preview_path, "wb") as f:
                writer_preview.write(f)

            # 4. Encrypt original full PDF
            log(f"{pdf_file} 암호화 중")
            
            # Save full PDF to bytes
            buffer = io.BytesIO()
            writer_full.write(buffer)
            buffer.seek(0)
            raw_pdf_bytes = buffer.read()

            # Prepare key and IV
            def prepare_bytes(text, size):
                b = text.encode("utf-8")
                return b + b'\x00' * (size - len(b)) if len(b) < size else b[:size]

            key = prepare_bytes("PassNote", 32)
            iv = prepare_bytes("newlearn", 16)

            cipher = AES.new(key, AES.MODE_CBC, iv)
            encrypted_bytes = cipher.encrypt(pad(raw_pdf_bytes, AES.block_size))
            encrypted_path = os.path.join(save_path, f"{name_without_ext}.pdf")

            with open(encrypted_path, "wb") as f:
                f.write(encrypted_bytes)

            # 5. Zip the files
            log(f"{pdf_file} 파일 저장 시작")
            zip_path = os.path.join(save_path, f"{name_without_ext}.zip")
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(jpg_path, arcname=f"{name_without_ext}.jpg")
                zipf.write(preview_path, arcname=f"{name_without_ext}_preview.pdf")
                zipf.write(encrypted_path, arcname=f"{name_without_ext}.pdf")
            
            os.remove(jpg_path)
            os.remove(preview_path)
            os.remove(encrypted_path)
            log(f"{pdf_file} 암호화 완료")
            return row

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_pdf_file, pdf_file) for pdf_file in pdf_files]
            for future in as_completed(futures):
                result = future.result()  # can handle errors or progress if needed
                progress["value"] += 1
                progress_status.config(text=f"{int(progress['value'])} / {len(pdf_files)} 완료됨")
                root.update_idletasks()

        data = [future.result() for future in futures]

        df = pd.DataFrame(data, columns=columns)
        
        
        log(f"최종파일 저장중(저장위치: {save_path})")
        if save_path:
            excel_path = os.path.join(save_path, "upload.xlsx")
            df.to_excel(excel_path, index=False)

            # 최종 zip 파일 만들기
            final_zip_path = os.path.join(save_path, "all_books.zip")
            with zipfile.ZipFile(final_zip_path, "w", zipfile.ZIP_DEFLATED) as final_zip:
                for file in os.listdir(save_path):
                    if file.endswith(".zip") and file != "all_books.zip":
                        file_path = os.path.join(save_path, file)
                        final_zip.write(file_path, arcname=file)
            
            # Delete individual zip files
            for file in os.listdir(save_path):
                if file.endswith(".zip") and file != "all_books.zip":
                    os.remove(os.path.join(save_path, file))
        elapsed = time.time() - start_time
        log(f"총 소요 시간: {elapsed:.2f}초")
        log("최종 업로드 파일 생성 완료")

    except Exception as e:
        messagebox.showerror("에러 발생", str(e))

def log(message):
    log_text.config(state='normal')
    log_text.insert(tk.END, message + '\n')
    log_text.see(tk.END)
    log_text.config(state='disabled')
    root.update_idletasks()

# GUI 구성
root = tk.Tk()
root.title("PDF 암호화 도구")
root.geometry("500x300")

def on_button_click():
    btn.config(state="disabled")
    def task():
        encrypt_pdfs()
        btn.config(state="normal")
    threading.Thread(target=task, daemon=True).start()

btn = tk.Button(root, text="pdf 폴더 선택", width=15, height=2)
btn.config(command=on_button_click)
btn.pack(padx=20, pady=10)


# Add progress bar and label in a horizontal frame
progress_frame = tk.Frame(root)
progress_frame.pack(padx=10, pady=5, fill="x", anchor = "center")

progress = ttk.Progressbar(progress_frame, orient="horizontal", length=350, mode="determinate")
progress.pack(side="left", fill="x", expand=True, padx=5, pady=2, ipady=3)

progress_status = tk.Label(progress_frame, text="0 / 0 완료됨")
progress_status.pack(side="left", padx=5)

log_text = scrolledtext.ScrolledText(root, width = 60, height=15, state="disabled")
log_text.pack(padx=10, pady=10)

root.mainloop()
