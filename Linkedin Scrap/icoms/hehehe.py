import pandas as pd

# Ubah path sesuai dengan path file CSV yang ingin diubah
csv_file = 'F:\Skripsi\Diagram\Linkedin Scrap\icoms\mydata.csv'

# Baca file CSV
df = pd.read_csv(csv_file)

# Ubah atau sesuaikan nama file Excel yang dihasilkan
excel_file = 'data_0.xlsx'

# Simpan ke dalam file Excel
df.to_excel(excel_file, index=False)

print(f"File Excel '{excel_file}' berhasil dibuat.")