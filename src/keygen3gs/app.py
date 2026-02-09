import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
import base64
import pyaes

# === KONFIGURASI ===
SECRET_KEY = b'rahasia2021Angga'
IV = b'InitializationVe'

def encrypt_license(hwid):
    try:
        # 1. BERSIHKAN INPUT (Sama persis PC)
        clean_hwid = "".join(hwid.split())
        data_bytes = clean_hwid.encode('utf-8')

        # 2. PADDING MANUAL (Rumus Matematika PKCS7)
        # Ini rahasianya biar Pyaes hasilnya SAMA dengan Cryptodome
        block_size = 16
        padding_len = block_size - (len(data_bytes) % block_size)
        padding = bytes([padding_len] * padding_len)
        padded_data = data_bytes + padding

        # 3. ENKRIPSI (Pure Python - Anti Crash)
        aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
        encrypter = pyaes.Encrypter(aes)
        
        ciphertext = encrypter.feed(padded_data)
        ciphertext += encrypter.feed() # Finalize
        
        # 4. HASIL
        return base64.b64encode(ciphertext).decode('utf-8')

    except Exception as e:
        return f"Error: {str(e)}"

class KeygenApp(toga.App):
    def startup(self):
        # Tampilan Gelap (Dark Mode)
        # Container Utama
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, background_color='#2b2b2b', alignment=CENTER))

        # Judul
        label_title = toga.Label(
            "PES 21 KEYGEN (OFFLINE)",
            style=Pack(padding=(0, 20), font_size=18, font_weight='bold', color='#B9F01D', text_align='center')
        )

        # Input
        self.input_hwid = toga.TextInput(
            placeholder="Tempel HWID disini...",
            style=Pack(padding=10, width=280, background_color='white', color='black')
        )

        # Tombol
        btn_generate = toga.Button(
            "GENERATE LISENSI",
            on_press=self.do_generate,
            style=Pack(padding=10, width=280, background_color='#00BFFF', color='white', font_weight='bold')
        )

        # Output
        self.input_result = toga.TextInput(
            readonly=True,
            placeholder="Hasil Lisensi...",
            style=Pack(padding=10, width=280, background_color='#dddddd', color='black')
        )
        
        # Tambahkan Widget
        main_box.add(label_title)
        main_box.add(self.input_hwid)
        main_box.add(toga.Divider(style=Pack(padding=(10,0))))
        main_box.add(btn_generate)
        main_box.add(toga.Divider(style=Pack(padding=(10,0))))
        main_box.add(self.input_result)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def do_generate(self, widget):
        hwid = self.input_hwid.value
        if hwid:
            # Panggil fungsi enkripsi manual tadi
            hasil = encrypt_license(hwid)
            self.input_result.value = hasil
        else:
            self.input_result.value = "HWID KOSONG!"

def main():
    return KeygenApp()
