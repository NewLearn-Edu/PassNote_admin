import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import zipfile
import random
import fitz  # PyMuPDF
import sys
 
sys.setrecursionlimit(sys.getrecursionlimit() * 5)


def encrypt_pdfs():
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

        # Create a DataFrame with required columns
        columns = ["Name", "Description", "Author", "Publisher", "PublicationDate", "Price", "Pages", "ISBN"]
        data = []

        # Create DataFrame after processing files
        for pdf_file in pdf_files:
            name_without_ext = os.path.splitext(pdf_file)[0]
            row = [name_without_ext] + [""] * (len(columns) - 1)
            data.append(row)

        df = pd.DataFrame(data, columns=columns)

        # Save path is set to folder_path (where PDFs are located)

        save_path = os.path.join(os.path.dirname(folder_path), "passNote_Upload")
        os.makedirs(save_path, exist_ok=True)

        for pdf_file in pdf_files:
            name_without_ext = os.path.splitext(pdf_file)[0]
            full_pdf_path = os.path.join(folder_path, pdf_file)

            # 1. Read PDF
            reader = PdfReader(full_pdf_path)
            writer_full = PdfWriter()
            for page in reader.pages:
                writer_full.add_page(page)

            # 2. Save first page as image using PyMuPDF
            doc = fitz.open(full_pdf_path)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            jpg_path = os.path.join(save_path, f"{name_without_ext}.jpg")
            pix.save(jpg_path)
            doc.close()

            # 3. Create preview PDF with 10% random pages
            num_pages = len(reader.pages)
            num_preview_pages = max(1, int(num_pages * 0.1))
            sampled_indices = sorted(random.sample(range(num_pages), num_preview_pages))
            writer_preview = PdfWriter()
            for idx in sampled_indices:
                writer_preview.add_page(reader.pages[idx])
            preview_path = os.path.join(save_path, f"{name_without_ext}_preview.pdf")
            with open(preview_path, "wb") as f:
                writer_preview.write(f)

            # 4. Encrypt original full PDF
            encrypted_path = os.path.join(save_path, f"{name_without_ext}.pdf")
            writer_full.encrypt("passnote")
            with open(encrypted_path, "wb") as f:
                writer_full.write(f)

            # 5. Zip the files
            zip_path = os.path.join(save_path, f"{name_without_ext}.zip")
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(jpg_path, arcname=f"{name_without_ext}.jpg")
                zipf.write(preview_path, arcname=f"{name_without_ext}_preview.pdf")
                zipf.write(encrypted_path, arcname=f"{name_without_ext}.pdf")
            
            os.remove(jpg_path)
            os.remove(preview_path)
            os.remove(encrypted_path)
            
            print(f"생성 완료: {zip_path}")

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


    except Exception as e:
        messagebox.showerror("에러 발생", str(e))

# GUI 구성
root = tk.Tk()
root.title("PDF 암호화 도구")
root.geometry("400x200")

btn = tk.Button(root, text="pdf 폴더 선", command=encrypt_pdfs, width=20, height=2)
btn.pack(padx=20, pady=20)

root.mainloop()