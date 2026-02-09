import flet as ft
import base64
import pyaes
import asyncio

# --- KONFIGURASI KEAMANAN (WAJIB SAMA DENGAN PC) ---
SECRET_KEY = b'rahasia2021Angga' 
IV = b'InitializationVe'          

class Security:
    @staticmethod
    def encrypt_license(hwid):
        try:
            # 1. PEMBERSIH SUPER (Hapus Spasi & Enter) 🧹
            # Masalah "Beda Hasil" biasanya karena ada spasi nyelip
            clean_text = "".join(hwid.split()) 
            data_bytes = clean_text.encode('utf-8')

            # 2. Padding PKCS7 Manual (Disamakan dengan Logic PC)
            # Rumus ini memastikan panjang data kelipatan 16 byte
            block_size = 16
            padding_len = block_size - (len(data_bytes) % block_size)
            padding = bytes([padding_len] * padding_len)
            padded_data = data_bytes + padding

            # 3. Enkripsi AES CBC (Pyaes Pure Python)
            aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
            encrypter = pyaes.Encrypter(aes)
            
            ciphertext = encrypter.feed(padded_data)
            ciphertext += encrypter.feed() # Finalize
            
            return base64.b64encode(ciphertext).decode('utf-8'), clean_text
        except Exception as e:
            return f"Error: {str(e)}", ""

def main(page: ft.Page):
    # Setup Layar
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark" 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    
    # Warna
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"
    
    # --- LOGIC ---
    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID Kosong!"
            page.update()
            return

        # Loading State
        btn_generate.text = "⏳ MEMPROSES..."
        btn_generate.disabled = True
        page.update()
        
        # Jeda biar UI ngerender
        await asyncio.sleep(0.1) 

        # Proses Enkripsi
        license_key, debug_text = Security.encrypt_license(txt_hwid.value)
        
        # Tampilkan Hasil
        txt_result.value = license_key
        
        # DEBUG INFO (Cek apakah inputnya sudah bersih?)
        lbl_debug.value = f"Input Bersih: [{debug_text}]"

        # Reset Tombol
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Selesai!")))
        page.update()

    async def paste_click(e):
        clipboard_text = await page.get_clipboard()
        if clipboard_text:
            # Bersihkan saat paste
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
    btn_generate = ft.ElevatedButton("GENERATE LISENSI", on_click=generate_click, bgcolor=BLUE_BTN, color="black")
    lbl_debug = ft.Text("", size=12, color="orange", italic=True) # Info Debug

    page.add(
        ft.Column([
            ft.Text("PES21 KEYGEN", size=24, color=NEON_GREEN, weight="bold"),
            ft.Container(height=20),
            txt_hwid,
            ft.ElevatedButton("Paste Clipboard", on_click=paste_click, bgcolor=NEON_GREEN, color="black"),
            ft.Container(height=10),
            btn_generate,
            lbl_debug, # Debug muncul disini
            ft.Container(height=10),
            txt_result,
            ft.ElevatedButton("Salin Lisensi", on_click=copy_click, bgcolor=NEON_GREEN, color="black"),
            ft.Container(height=30),
            ft.Text("© 2026 3GS Patch", size=10, color="grey")
        ], horizontal_alignment="center")
    )

ft.app(target=main)
