import flet as ft
import base64
import pyaes  # <--- Kita pakai library ini, lebih aman buat Android

# === KONFIGURASI KEAMANAN ===
SECRET_KEY = bytes([114, 97, 104, 97, 115, 105, 97, 50, 48, 50, 49, 65, 110, 103, 103, 97]) # rahasia2021Angga
IV = bytes([73, 110, 105, 116, 105, 97, 108, 105, 122, 97, 116, 105, 111, 110, 86, 101])     # InitializationVe

class Security:
    @staticmethod
    def encrypt_license(hwid):
        try:
            # 1. Padding Manual (PKCS7) - Pengganti pad() dari Crypto
            block_size = 16
            data_bytes = hwid.encode('utf-8')
            padding_len = block_size - (len(data_bytes) % block_size)
            padding = bytes([padding_len] * padding_len)
            padded_data = data_bytes + padding

            # 2. Enkripsi pakai Pyaes (Pure Python)
            aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
            encrypter = pyaes.Encrypter(aes)
            
            encrypted = encrypter.feed(padded_data)
            encrypted += encrypter.feed() # Finalize
            
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"

def main(page: ft.Page):
    # --- SETUP TAMPILAN ---
    page.title = "3GS Keygen 21"
    page.theme_mode = "dark" 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_width = 400
    page.window_height = 700
    
    # Warna Tema
    NEON_GREEN = "#B9F01D"
    DARK_BG = "#263238" 
    BLUE_BTN = "#2196F3"
    
    # --- FUNGSI TOMBOL ---
    def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID tidak boleh kosong!"
            page.update()
        else:
            txt_hwid.error_text = None
            license_key = Security.encrypt_license(txt_hwid.value)
            txt_result.value = license_key
            
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Lisensi Berhasil Dibuat!"), bgcolor="green")
            )
            page.update()

    async def paste_click(e):
        clipboard_text = await page.get_clipboard()
        if clipboard_text:
            txt_hwid.value = clipboard_text
            txt_hwid.error_text = None
            page.show_snack_bar(ft.SnackBar(content=ft.Text("HWID Ditempel!")))
            page.update()

    def copy_click(e):
        if txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Lisensi Disalin ke Clipboard!")))
        else:
             page.show_snack_bar(ft.SnackBar(content=ft.Text("Belum ada lisensi!"), bgcolor="red"))

    # --- KOMPONEN UI ---
    
    # 1. Judul
    lbl_title = ft.Text("3GS KEY GENERATOR", size=24, weight="bold", color=NEON_GREEN)
    lbl_subtitle = ft.Text("Khusus Admin/Penjual", size=12, color="grey")

    # 2. Input HWID
    txt_hwid = ft.TextField(
        label="Tempel HWID Pembeli",
        hint_text="Tempel di sini...",
        icon="fingerprint",
        border_color=NEON_GREEN,
        focused_border_color=NEON_GREEN,
    )

    # 3. Tombol Paste
    btn_paste = ft.ElevatedButton(
        "Tempel dari Clipboard",
        icon="paste",
        on_click=paste_click,
        bgcolor=DARK_BG,
        color="white",
        width=280
    )

    # 4. Tombol Generate
    btn_generate = ft.ElevatedButton(
        "GENERATE LISENSI",
        icon="key",
        on_click=generate_click,
        bgcolor=NEON_GREEN,
        color="black",
        width=280,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    # 5. Output Hasil
    txt_result = ft.TextField(
        label="Hasil Lisensi",
        read_only=True,
        multiline=True,
        icon="lock_open",
        border_color=BLUE_BTN,
    )

    # 6. Tombol Copy
    btn_copy = ft.ElevatedButton(
        "Salin Lisensi",
        icon="copy",
        on_click=copy_click,
        bgcolor=BLUE_BTN,
        color="white",
        width=280
    )

    # 7. Copyright
    lbl_copy = ft.Text("© 2026 - 3GS Patch", size=10, color="grey")

    # --- MENYUSUN LAYOUT ---
    page.add(
        ft.Column(
            [
                ft.Container(height=20),
                lbl_title,
                lbl_subtitle,
                ft.Container(height=20),
                txt_hwid,
                btn_paste,
                ft.Container(height=10),
                btn_generate,
                ft.Container(height=20),
                txt_result,
                btn_copy,
                ft.Container(height=30),
                lbl_copy
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    )

ft.app(target=main)
