import flet as ft
import base64
import pyaes
import asyncio

# ==========================================
# KONFIGURASI KEAMANAN (SAMA PERSIS DENGAN PC)
# ==========================================
# Pastikan ini Byte Literal (b'...') agar sama dengan PC
SECRET_KEY = b'rahasia2021Angga' 
IV = b'InitializationVe'          

class Security:
    @staticmethod
    def encrypt_license(hwid):
        try:
            # 1. Bersihkan Input (Hapus spasi depan/belakang)
            # Seringkali hasil beda karena ada spasi yang tidak sengaja ter-copy
            text = hwid.strip()
            data_bytes = text.encode('utf-8')

            # 2. Padding PKCS7 Manual (Meniru logic Cryptodome.Util.Padding.pad)
            # Ini memastikan hasil matematika-nya 100% sama dengan versi PC
            block_size = 16
            padding_len = block_size - (len(data_bytes) % block_size)
            padding = bytes([padding_len] * padding_len)
            padded_data = data_bytes + padding

            # 3. Enkripsi AES CBC Mode
            # Kita buat objek baru setiap kali encrypt agar IV reset
            aes = pyaes.AESModeOfOperationCBC(SECRET_KEY, iv=IV)
            encrypter = pyaes.Encrypter(aes)
            
            ciphertext = encrypter.feed(padded_data)
            ciphertext += encrypter.feed() # Finalize
            
            return base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"

def main(page: ft.Page):
    # --- SETUP TAMPILAN ---
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark" 
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_width = 400
    page.window_height = 700
    page.padding = 20
    
    # Warna Tema (Samakan Nuansa dengan PC)
    NEON_GREEN = "#B9F01D" # Warna aksen hijau
    DARK_BG = "#2b2b2b" 
    BLUE_BTN = "#00BFFF"
    
    # --- FUNGSI LOGIC ---
    async def generate_click(e):
        # Validasi Input
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID tidak boleh kosong!"
            page.update()
            return

        # 1. UI FEEDBACK: Ubah tombol jadi "Memproses..." biar user sabar
        btn_generate.text = "Memproses..."
        btn_generate.disabled = True
        txt_hwid.error_text = None
        page.update()

        # Beri jeda sedikit agar UI sempat ter-update sebelum proses berat dimulai
        await asyncio.sleep(0.1) 

        # 2. PROSES ENKRIPSI
        # Kita panggil logic keamanan
        license_key = Security.encrypt_license(txt_hwid.value)
        
        # 3. TAMPILKAN HASIL
        txt_result.value = license_key
        
        # Kembalikan tombol seperti semula
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        
        page.show_snack_bar(
            ft.SnackBar(content=ft.Text("Lisensi Berhasil Dibuat!"), bgcolor="green")
        )
        page.update()

    async def paste_click(e):
        clipboard_text = await page.get_clipboard()
        if clipboard_text:
            # Otomatis strip spasi saat paste
            clean_text = clipboard_text.strip()
            txt_hwid.value = clean_text
            txt_hwid.error_text = None
            page.show_snack_bar(ft.SnackBar(content=ft.Text("HWID Ditempel!")))
            page.update()

    def copy_click(e):
        if txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Disalin ke Clipboard!")))
        else:
             page.show_snack_bar(ft.SnackBar(content=ft.Text("Belum ada lisensi!"), bgcolor="red"))

    # --- KOMPONEN UI (LAYOUT) ---
    
    # Judul
    lbl_title = ft.Text("PES21 KEY-GENERATOR", size=24, weight="bold", color=NEON_GREEN)
    lbl_subtitle = ft.Text("KHUSUS ADMIN/PENJUAL", size=12, color="grey")

    # Input HWID
    txt_hwid = ft.TextField(
        label="HWID Pengguna",
        hint_text="Tempel HWID disini...",
        text_align=ft.TextAlign.CENTER,
        border_color=NEON_GREEN,
        bgcolor="#4a4a4a",
        text_size=14,
        focused_border_color=NEON_GREEN,
    )

    # Tombol Paste
    btn_paste = ft.ElevatedButton(
        "Tempel dari Clipboard",
        icon="paste",
        on_click=paste_click,
        bgcolor=NEON_GREEN,
        color="black",
        width=280,
        height=45
    )

    # Tombol Generate
    btn_generate = ft.ElevatedButton(
        "GENERATE LISENSI",
        icon="vpn_key",
        on_click=generate_click,
        bgcolor=BLUE_BTN,
        color="black",
        width=280,
        height=60, # Tombol besar seperti di PC
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=15),
        )
    )

    # Output Hasil
    txt_result = ft.TextField(
        label="Hasil Lisensi",
        read_only=True,
        multiline=True,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#4a4a4a",
        border_color=BLUE_BTN,
    )

    # Tombol Copy
    btn_copy = ft.ElevatedButton(
        "SALIN LISENSI",
        icon="copy",
        on_click=copy_click,
        bgcolor=NEON_GREEN,
        color="black",
        width=280,
        height=50
    )

    # Copyright
    lbl_copy = ft.Text("© 2026 - 3GS Patch", size=10, color="grey")

    # Menyusun Widget
    page.add(
        ft.Column(
            [
                ft.Container(height=10),
                lbl_title,
                lbl_subtitle,
                ft.Container(height=20),
                
                ft.Text("Masukan HWID Pengguna :", color="white"),
                txt_hwid,
                btn_paste,
                
                ft.Container(height=20),
                btn_generate,
                ft.Container(height=20),
                
                ft.Text("Kode Lisensi (Hasil) :", color="white"),
                txt_result,
                btn_copy,
                
                ft.Container(height=30),
                lbl_copy
            ],
            alignment="center",
            horizontal_alignment="center",
            scroll="adaptive" # Biar bisa di-scroll kalau layar HP kecil
        )
    )

ft.app(target=main)
