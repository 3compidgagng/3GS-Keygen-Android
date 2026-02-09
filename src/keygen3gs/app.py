import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
import base64
import pyaes

# --- KONFIGURASI KEAMANAN ---
SECRET_KEY = b'rahasia2021Angga'
IV = b'InitializationVe'

def encrypt_license(hwid):
    try:
        # 1. Bersihkan Input (Hapus spasi & enter)
        # Biar hasil 100% sama kayak PC
        clean_hwid = "".join(hwid.split()) 
        data_bytes = clean_hwid.encode('utf-8')

        # 2. Padding PKCS7 Manual (Standar PC)
        block_size = 16
        padding_len = block_size - (len(data_bytes) % block_size)
        padding = bytes([padding_len] * padding_len)
        padded_data = data_bytes + padding

        # 3. Enkripsi AES CBC (Pake Pyaes - Pure Python)
        aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
        encrypter = pyaes.Encrypter(aes)
        
        ciphertext = encrypter.feed(padded_data)
        ciphertext += encrypter.feed() # Finalize
        
        return base64.b64encode(ciphertext).decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"

class KeygenApp(toga.App):
    def startup(self):
        # Container Utama (Background Gelap)
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER, background_color='#2b2b2b'))

        # 1. Judul
        label_title = toga.Label(
            "PES 21 KEYGEN",
            style=Pack(padding=(0, 20), font_size=20, font_weight='bold', color='#B9F01D', text_align='center')
        )

        # 2. Input HWID
        self.input_hwid = toga.TextInput(
            placeholder="Tempel HWID disini...",
            style=Pack(padding=10, width=250, background_color='#ffffff', color='#000000')
        )

        # 3. Tombol Generate
        btn_generate = toga.Button(
            "GENERATE LISENSI",
            on_press=self.do_generate,
            style=Pack(padding=10, width=250, background_color='#00BFFF', color='white', font_weight='bold')
        )

        # 4. Output Hasil
        self.input_result = toga.TextInput(
            readonly=True,
            placeholder="Hasil akan muncul disini",
            style=Pack(padding=10, width=250, background_color='#dddddd', color='#000000')
        )
        
        # Tambahkan ke Layar
        main_box.add(label_title)
        main_box.add(self.input_hwid)
        main_box.add(toga.Divider(style=Pack(padding=(20,0)))) # Garis pembatas
        main_box.add(btn_generate)
        main_box.add(toga.Divider(style=Pack(padding=(10,0))))
        main_box.add(self.input_result)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def do_generate(self, widget):
        hwid = self.input_hwid.value
        if not hwid:
            self.input_result.value = "HWID KOSONG!"
            return
        
        # Panggil logic enkripsi
        self.input_result.value = "Memproses..."
        hasil = encrypt_license(hwid)
        self.input_result.value = hasil

def main():
    return KeygenApp()
