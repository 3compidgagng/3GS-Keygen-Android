import base64
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast

# === LIBRARY KEAMANAN (SAMA PERSIS DENGAN PC) ===
# Kita tetap pakai Cryptodome
from Cryptodome.Cipher import AES 
from Cryptodome.Util.Padding import pad

# === CONFIG KEAMANAN (WAJIB SAMA DENGAN LAUNCHER NUITKA) ===
# Gunakan Byte Array agar konsisten
SECRET_KEY = bytes([114, 97, 104, 97, 115, 105, 97, 50, 48, 50, 49, 65, 110, 103, 103, 97]) # rahasia2021Angga
IV = bytes([73, 110, 105, 116, 105, 97, 108, 105, 122, 97, 116, 105, 111, 110, 86, 101])     # InitializationVe

class Security:
    @staticmethod
    def encrypt_license(hwid):
        try:
            cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
            padded_hwid = pad(hwid.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_hwid)
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            return "Error Enkripsi"

class KeygenApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Dark"
        
        screen = Screen()
        
        # Layout Utama
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, adaptive_height=True)
        layout.pos_hint = {"center_x": .5, "center_y": .6}

        # 1. Judul
        label_title = MDLabel(text="3GS KEY GENERATOR", halign="center", theme_text_color="Custom", text_color=(0.73, 0.94, 0.11, 1), font_style="H5")
        layout.add_widget(label_title)
        
        label_subtitle = MDLabel(text="Khusus Admin/Penjual", halign="center", theme_text_color="Hint", font_style="Caption")
        layout.add_widget(label_subtitle)

        # 2. Input HWID
        self.input_hwid = MDTextField(
            hint_text="Tempel HWID Pembeli",
            helper_text="Tekan tahan untuk paste",
            helper_text_mode="on_focus",
            icon_right="fingerprint",
            icon_right_color=(0.73, 0.94, 0.11, 1),
            multiline=False
        )
        layout.add_widget(self.input_hwid)

        # 3. Tombol Paste
        btn_paste = MDFillRoundFlatButton(
            text="TEMPEL DARI CLIPBOARD",
            font_size=14,
            pos_hint={"center_x": .5},
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        btn_paste.bind(on_release=self.do_paste)
        layout.add_widget(btn_paste)

        # 4. Tombol Generate
        btn_gen = MDFillRoundFlatButton(
            text="GENERATE LISENSI",
            font_size=18,
            pos_hint={"center_x": .5},
            md_bg_color=(0.73, 0.94, 0.11, 1),
            text_color=(0, 0, 0, 1)
        )
        btn_gen.bind(on_release=self.do_generate)
        layout.add_widget(btn_gen)

        # 5. Output Result
        self.input_result = MDTextField(
            hint_text="Hasil Lisensi",
            readonly=True,
            multiline=False
        )
        layout.add_widget(self.input_result)

        # 6. Tombol Copy
        btn_copy = MDFillRoundFlatButton(
            text="SALIN LISENSI",
            pos_hint={"center_x": .5},
            md_bg_color=(0.2, 0.6, 0.8, 1)
        )
        btn_copy.bind(on_release=self.do_copy)
        layout.add_widget(btn_copy)

        screen.add_widget(layout)
        
        # Copyright footer
        label_copy = MDLabel(
            text="© 2026 - 3GS Patch", 
            halign="center", 
            pos_hint={"center_x": .5, "y": 0.05},
            theme_text_color="Hint",
            font_style="Caption"
        )
        screen.add_widget(label_copy)

        return screen

    def do_paste(self, instance):
        try:
            text = Clipboard.paste()
            if text:
                self.input_hwid.text = text
                toast("HWID Ditempel")
        except: pass

    def do_generate(self, instance):
        hwid = self.input_hwid.text.strip()
        if not hwid:
            self.input_hwid.error = True
            toast("HWID Kosong!")
            return
        
        license_key = Security.encrypt_license(hwid)
        self.input_result.text = license_key
        toast("Lisensi Dibuat!")

    def do_copy(self, instance):
        res = self.input_result.text
        if res:
            Clipboard.copy(res)
            toast("Lisensi Disalin!")

if __name__ == "__main__":
    KeygenApp().run()