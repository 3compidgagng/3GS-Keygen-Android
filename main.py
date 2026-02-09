import flet as ft
import base64
import pyaes
import asyncio

# ==========================================
# KONFIGURASI KEAMANAN
# ==========================================
SECRET_KEY = b'rahasia2021Angga' 
IV = b'InitializationVe'          

class Security:
    @staticmethod
    def encrypt_license(hwid):
        try:
            # 1. PEMBERSIH SUPER (Anti Karakter Hantu) 🧹
            # Kita paksa buang spasi, tab, enter, dan karakter aneh
            # HWID biasanya cuma huruf dan angka, jadi aman.
            text = hwid.strip().replace('\r', '').replace('\n', '').replace(' ', '')
            
            # Debugging: Print ke terminal (kalau ada) untuk cek
            print(f"DEBUG: Teks bersih = '{text}' (Panjang: {len(text)})")
            
            data_bytes = text.encode('utf-8')

            # 2. Padding PKCS7 Manual
            block_size = 16
            padding_len = block_size - (len(data_bytes) % block_size)
            padding = bytes([padding_len] * padding_len)
            padded_data = data_bytes + padding

            # 3. Enkripsi AES CBC
            aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
            encrypter = pyaes.Encrypter(aes)
            
            ciphertext = encrypter.feed(padded_data)
            ciphertext += encrypter.feed() # Finalize
            
            return base64.b64encode(ciphertext).decode('utf-8'), text
        except Exception as e:
            return f"Error: {str(e)}", ""

def main(page: ft.Page):
    # --- SETUP TAMPILAN ---
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark" 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_width = 400
    page.window_height = 700
    page.padding = 20
    
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"
    
    # --- FUNGSI LOGIC ---
    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID kosong!"
            page.update()
            return

        # UI Loading
        btn_generate.text = "⏳ Memproses..."
        btn_generate.disabled = True
        txt_hwid.error_text = None
        txt_debug.value = "Memulai..." # Reset debug
        page.update()

        # Jeda biar UI ngerender dulu
        await asyncio.sleep(0.1) 

        # PROSES ENKRIPSI
        # Kita terima 2 hasil: Lisensi & Teks Bersih (buat debug)
        license_key, clean_text = Security.encrypt_license(txt_hwid.value)
        
        # TAMPILKAN HASIL
        txt_result.value = license_key
        
        # TAMPILKAN INFO DEBUG (Penting buat cek kenapa beda)
        txt_debug.value = f"Input Bersih: '{clean_text}'\nPanjang Karakter: {len(clean_text)}"
        
        # Reset Tombol
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        
        page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Selesai!"), bgcolor="green")
        )
        page.update()

    async def paste_click(e):
        clipboard_text = await page.get_clipboard()
        if clipboard_text:
            # Langsung bersihkan saat paste
            clean_text = clipboard_text.strip().replace('\r', '').replace('\n', '')
            txt_hwid.value = clean_text
            txt_hwid.error_text = None
            page.show_snack_bar(ft.SnackBar(content=ft.Text("HWID Ditempel!")))
            page.update()

    def copy_click(e):
        if txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Disalin!")))

    # --- KOMPONEN UI ---
    
    lbl_title = ft.Text("PES21 KEY-GENERATOR", size=24, weight="bold", color=NEON_GREEN)
    
    txt_hwid = ft.TextField(
        label="HWID Pengguna",
        hint_text="Tempel HWID...",
        text_align=ft.TextAlign.CENTER,
        border_color=NEON_GREEN,
        bgcolor="#4a4a4a",
        text_size=14
    )

    btn_paste = ft.ElevatedButton("Tempel Clipboard", icon="paste", on_click=paste_click, bgcolor=NEON_GREEN, color="black", width=280)

    btn_generate = ft.ElevatedButton("GENERATE LISENSI", icon="vpn_key", on_click=generate_click, bgcolor=BLUE_BTN, color="black", width=280, height=50)

    txt_result = ft.TextField(
        label="Hasil Lisensi",
        read_only=True,
        multiline=True,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#4a4a4a",
        border_color=BLUE_BTN,
    )

    # INFO DEBUG (Supaya Mas bisa cek inputnya benar/salah)
    txt_debug = ft.Text(
        "Info Debug akan muncul disini...",
        size=12,
        color="orange",
        text_align=ft.TextAlign.CENTER,
        italic=True
    )

    btn_copy = ft.ElevatedButton("SALIN LISENSI", icon="copy", on_click=copy_click, bgcolor=NEON_GREEN, color="black", width=280)

    page.add(
        ft.Column(
            [
                ft.Container(height=10),
                lbl_title,
                ft.Text("KHUSUS ADMIN", size=12, color="grey"),
                ft.Container(height=20),
                txt_hwid,
                btn_paste,
                ft.Container(height=20),
                btn_generate,
                ft.Container(height=10),
                txt_debug, # <--- Posisi Debug Info
                ft.Container(height=10),
                txt_result,
                btn_copy,
                ft.Container(height=30),
                ft.Text("© 2026 - 3GS Patch", size=10, color="grey")
            ],
            alignment="center",
            horizontal_alignment="center",
            scroll="adaptive"
        )
    )

ft.app(target=main)
