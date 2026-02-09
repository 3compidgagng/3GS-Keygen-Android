import flet as ft
import base64
import asyncio
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# --- KONFIGURASI KEAMANAN ---
SECRET_KEY = b'rahasia2021Angga' 
IV = b'InitializationVe'          

class Security:
    @staticmethod
    def encrypt_license(hwid):
        try:
            # 1. Bersihkan Input
            clean_text = "".join(hwid.split())
            data_bytes = clean_text.encode('utf-8')

            # 2. Padding PKCS7 (Cara Resmi Library Cryptography)
            # Ini jauh lebih aman dan standar daripada hitung manual
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data_bytes) + padder.finalize()

            # 3. Enkripsi AES CBC
            cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CBC(IV), backend=default_backend())
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            
            return base64.b64encode(ciphertext).decode('utf-8'), clean_text
        except Exception as e:
            return f"Error: {str(e)}", ""

def main(page: ft.Page):
    # --- SETUP TAMPILAN ---
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark" 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto" 
    
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"
    
    # --- LOGIC ---
    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID kosong!"
            page.update()
            return

        btn_generate.text = "⏳ MEMPROSES..."
        btn_generate.disabled = True
        page.update()
        await asyncio.sleep(0.1) 

        # Enkripsi
        license_key, debug_text = Security.encrypt_license(txt_hwid.value)
        
        txt_result.value = license_key
        lbl_debug.value = f"Input Bersih: '{debug_text}'"

        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Selesai!")))
        page.update()

    async def paste_click(e):
        clipboard_text = await page.get_clipboard()
        if clipboard_text:
            clean = "".join(clipboard_text.split())
            txt_hwid.value = clean
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Ditempel!")))
            page.update()

    def copy_click(e):
        if txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Disalin!")))

    # --- UI ---
    txt_hwid = ft.TextField(label="HWID", text_align=ft.TextAlign.CENTER, border_color=NEON_GREEN)
    txt_result = ft.TextField(label="Lisensi", read_only=True, text_align=ft.TextAlign.CENTER, border_color=BLUE_BTN)
    btn_generate = ft.ElevatedButton("GENERATE", on_click=generate_click, bgcolor=BLUE_BTN, color="black")
    lbl_debug = ft.Text("", size=10, color="orange")

    page.add(
        ft.Column([
            ft.Text("PES21 KEYGEN", size=24, color=NEON_GREEN, weight="bold"),
            ft.Container(height=20),
            txt_hwid,
            ft.ElevatedButton("Paste", on_click=paste_click, bgcolor=NEON_GREEN, color="black"),
            ft.Container(height=10),
            btn_generate,
            lbl_debug,
            ft.Container(height=10),
            txt_result,
            ft.ElevatedButton("Copy", on_click=copy_click, bgcolor=NEON_GREEN, color="black"),
            ft.Container(height=30),
            ft.Text("© 2026 3GS Patch", size=10, color="grey")
        ], horizontal_alignment="center")
    )

ft.app(target=main)
