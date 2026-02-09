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
            # 1. PEMBERSIH SUPER AGRESIF 🧹
            # Kita buang spasi ( ), Enter (\n), Tab (\t), dan Carriage Return (\r)
            # Ini kuncinya biar hasilnya sama dengan PC!
            clean_text = "".join(hwid.split()) 
            
            # Ubah ke bytes
            data_bytes = clean_text.encode('utf-8')

            # 2. Padding PKCS7 Manual (Standar Industri)
            block_size = 16
            padding_len = block_size - (len(data_bytes) % block_size)
            padding = bytes([padding_len] * padding_len)
            padded_data = data_bytes + padding

            # 3. Enkripsi AES CBC
            aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
            encrypter = pyaes.Encrypter(aes)
            
            ciphertext = encrypter.feed(padded_data)
            ciphertext += encrypter.feed() # Finalize
            
            return base64.b64encode(ciphertext).decode('utf-8'), clean_text
        except Exception as e:
            return f"Error: {str(e)}", ""

def main(page: ft.Page):
    # --- SETUP TAMPILAN ---
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark" 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    # Scroll diset 'auto' biar kalau keyboard muncul, layar bisa digeser
    page.scroll = "auto" 
    
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"
    
    # --- LOGIC APLIKASI ---
    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID kosong!"
            page.update()
            return

        # Tampilkan Loading
        btn_generate.text = "⏳ SEDANG MEMPROSES..."
        btn_generate.disabled = True
        txt_result.value = "Mohon tunggu..."
        page.update()

        # Jeda dikit biar UI ngerender
        await asyncio.sleep(0.1) 

        # Proses Enkripsi
        license_key, debug_text = Security.encrypt_license(txt_hwid.value)
        
        # Tampilkan Hasil
        txt_result.value = license_key
        
        # Info Debug (Buat ngecek apa yang sebenernya dienkripsi)
        lbl_debug.value = f"Data yang dienkripsi: '{debug_text}'"

        # Balikin Tombol
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Selesai!")))
        page.update()

    async def paste_click(e):
        clipboard_text = await page.get_clipboard()
        if clipboard_text:
            # Langsung bersihkan saat ditempel
            clean = "".join(clipboard_text.split())
            txt_hwid.value = clean
            txt_hwid.error_text = None
            page.show_snack_bar(ft.SnackBar(content=ft.Text("HWID Ditempel!")))
            page.update()

    def copy_click(e):
        if txt_result.value and "Error" not in txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Lisensi Disalin!")))

    # --- KOMPONEN UI ---
    
    lbl_title = ft.Text("PES21 KEY-GENERATOR", size=24, weight="bold", color=NEON_GREEN)
    
    txt_hwid = ft.TextField(
        label="HWID Pengguna",
        hint_text="Tempel HWID disini...",
        text_align=ft.TextAlign.CENTER,
        border_color=NEON_GREEN,
        text_size=16
    )

    btn_paste = ft.ElevatedButton("Tempel dari Clipboard", icon="paste", on_click=paste_click, bgcolor=NEON_GREEN, color="black", width=280)

    btn_generate = ft.ElevatedButton("GENERATE LISENSI", icon="vpn_key", on_click=generate_click, bgcolor=BLUE_BTN, color="black", width=280, height=50)

    txt_result = ft.TextField(
        label="Hasil Lisensi",
        read_only=True,
        multiline=True,
        text_align=ft.TextAlign.CENTER,
        border_color=BLUE_BTN,
        text_size=16
    )

    btn_copy = ft.ElevatedButton("SALIN LISENSI", icon="copy", on_click=copy_click, bgcolor=NEON_GREEN, color="black", width=280)

    lbl_debug = ft.Text("", size=10, color="grey", italic=True)

    # Susun Layout
    page.add(
        ft.Column(
            [
                ft.Container(height=20),
                lbl_title,
                ft.Text("KHUSUS ADMIN", size=12, color="grey"),
                ft.Container(height=30),
                txt_hwid,
                btn_paste,
                ft.Container(height=20),
                btn_generate,
                ft.Container(height=10),
                lbl_debug, # Info debug muncul disini
                ft.Container(height=10),
                txt_result,
                btn_copy,
                ft.Container(height=50),
            ],
            horizontal_alignment="center",
        )
    )

ft.app(target=main)
