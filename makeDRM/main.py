import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import zipfile

def encrypt_pdfs():
    try:
        # Load Excel file
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not file_path:
            return

        df = pd.read_excel(file_path)
        if '책이름' not in df.columns:
            messagebox.showerror("에러", "'책이름' 컬럼이 엑셀 파일에 없습니다.")
            return

        book_titles = df['책이름'].dropna().tolist()

        input_folder = os.path.join(os.getcwd(), "pdf")
        output_folder = os.path.join(os.getcwd(), "pdfs")
        os.makedirs(output_folder, exist_ok=True)

        for title in book_titles:
            input_path = os.path.join(input_folder, f"{title}.pdf")
            output_path = os.path.join(output_folder, f"{title}.pdf")

            if not os.path.exists(input_path):
                print(f"파일 없음: {input_path}")
                continue

            reader = PdfReader(input_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt("passnote")  # 암호 설정
            with open(output_path, "wb") as f:
                writer.write(f)

        import zipfile

        zip_path = os.path.join(os.getcwd(), "encrypted_package.zip")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add the Excel file
            zipf.write(file_path, arcname=os.path.basename(file_path))

            # Add files from the output folder
            for filename in os.listdir(output_folder):
                file_full_path = os.path.join(output_folder, filename)
                zipf.write(file_full_path, arcname=os.path.join("pdfs", filename))

        messagebox.showinfo("완료", "PDF 암호화가 완료되었습니다.")

    except Exception as e:
        messagebox.showerror("에러 발생", str(e))

# GUI 구성
root = tk.Tk()
root.title("PDF 암호화 도구")

btn = tk.Button(root, text="엑셀 파일 선택 후 PDF 암호화", command=encrypt_pdfs)
btn.pack(padx=20, pady=20)

root.mainloop()