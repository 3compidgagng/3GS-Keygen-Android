import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import base64

# --- LOGIC KEAMANAN PC (SAMA PERSIS) ---
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
except ImportError:
    # Fallback kalau library belum ke-load (buat debug)
    AES = None

SECRET_KEY = b'rahasia2021Angga'
IV = b'InitializationVe'

def encrypt_license(hwid):
    if not AES:
        return "Error: Library Crypto tidak ditemukan"
    try:
        clean_hwid = "".join(hwid.split()) # Hapus spasi
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
        padded_hwid = pad(clean_hwid.encode('utf-8'), AES.block_size)
        encrypted = cipher.encrypt(padded_hwid)
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        return f"Error: {str(e)}"

class KeygenApp(toga.App):
    def startup(self):
        # Container Utama
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER, background_color='#2b2b2b'))

        # 1. Judul
        label_title = toga.Label(
            "PES 21 KEYGEN",
            style=Pack(padding=(0, 20), font_size=20, font_weight='bold', color='#B9F01D')
        )

        # 2. Input HWID
        self.input_hwid = toga.TextInput(
            placeholder="Tempel HWID disini...",
            style=Pack(padding=10, width=300, background_color='#ffffff')
        )

        # 3. Tombol Generate
        btn_generate = toga.Button(
            "GENERATE LISENSI",
            on_press=self.do_generate,
            style=Pack(padding=10, width=200, background_color='#00BFFF', color='white')
        )

        # 4. Output Hasil
        self.input_result = toga.TextInput(
            readonly=True,
            style=Pack(padding=10, width=300, background_color='#dddddd')
        )

        # 5. Tombol Copy
        btn_copy = toga.Button(
            "SALIN LISENSI",
            on_press=self.do_copy,
            style=Pack(padding=10, width=200, background_color='#B9F01D', color='black')
        )
        
        # Tambahkan ke Layar
        main_box.add(label_title)
        main_box.add(self.input_hwid)
        main_box.add(btn_generate)
        main_box.add(toga.Divider(style=Pack(padding=(20,0))))
        main_box.add(self.input_result)
        main_box.add(btn_copy)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def do_generate(self, widget):
        hwid = self.input_hwid.value
        if not hwid:
            self.input_result.value = "HWID KOSONG!"
            return
        
        # Panggil logic enkripsi
        hasil = encrypt_license(hwid)
        self.input_result.value = hasil

    def do_copy(self, widget):
        # BeeWare belum punya fitur clipboard bawaan yang stabil di semua android
        # Jadi kita akali dengan select all text biar user copy manual
        self.input_result.focus()

def main():
    return KeygenApp()
