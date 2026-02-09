import flet as ft
import requests
import asyncio

# URL Server Mas
API_URL = "https://3gs21pes.pythonanywhere.com/generate"

def main(page: ft.Page):
    # Setup Layar
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto" # Biar bisa discroll kalau keyboard muncul
    
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"

    # --- FUNGSI GENERATE ---
    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID Kosong!"
            page.update()
            return

        # UI Loading
        btn_generate.text = "⏳ MENGHUBUNGI SERVER..."
        btn_generate.disabled = True
        txt_result.value = "Sedang memproses..."
        page.update()
        
        try:
            # Kirim Data ke Server
            # verify=False : Biar Android tidak memblokir koneksi SSL
            # timeout=20   : Waktu tunggu maksimal 20 detik
            response = requests.post(
                API_URL, 
                json={"hwid": txt_hwid.value}, 
                timeout=20, 
                verify=False 
            )
            
            # Cek Jawaban
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'sukses':
                    txt_result.value = data['license']
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Sukses Dibuat!"), bgcolor="green"))
                else:
                    txt_result.value = f"Gagal: {data.get('pesan')}"
            else:
                txt_result.value = f"Error Server: {response.status_code}"
                
        except Exception as err:
            txt_result.value = f"Gagal Koneksi:\n{str(err)}"
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Cek Internet Anda"), bgcolor="red"))

        # Reset Tombol
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        page.update()

    # --- FUNGSI PASTE ---
    async def paste_click(e):
        clip = await page.get_clipboard_async()
        if clip:
            # Bersihkan spasi
            clean = "".join(clip.split())
            txt_hwid.value = clean
            page.show_snack_bar(ft.SnackBar(content=ft.Text("HWID Ditempel!")))
            page.update()

    # --- FUNGSI COPY ---
    def copy_click(e):
        if txt_result.value and "Gagal" not in txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Lisensi Disalin!")))

    # --- UI ---
    txt_hwid = ft.TextField(label="HWID Pengguna", text_align=ft.TextAlign.CENTER, border_color=NEON_GREEN)
    txt_result = ft.TextField(
        label="Hasil Lisensi", 
        read_only=True, 
        text_align=ft.TextAlign.CENTER, 
        border_color=BLUE_BTN,
        multiline=True,
        text_size=12
    )

    btn_generate = ft.ElevatedButton("GENERATE LISENSI", on_click=generate_click, bgcolor=BLUE_BTN, color="black", width=200)

    page.add(
        ft.Column([
            ft.Text("PES21 KEYGEN (ONLINE)", size=24, color=NEON_GREEN, weight="bold"),
            ft.Container(height=20),
            txt_hwid,
            ft.ElevatedButton("Tempel HWID", on_click=paste_click, bgcolor=NEON_GREEN, color="black"),
            ft.Container(height=10),
            btn_generate,
            ft.Container(height=10),
            txt_result,
            ft.ElevatedButton("Salin Lisensi", on_click=copy_click, bgcolor=NEON_GREEN, color="black"),
            ft.Container(height=20),
            ft.Text("© 2026 3GS Patch", size=10, color="grey")
        ], horizontal_alignment="center")
    )

ft.app(target=main)
