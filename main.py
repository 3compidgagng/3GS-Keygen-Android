import flet as ft
import requests # Library buat nelpon server
import asyncio

# URL SERVER MAS YANG SUDAH AKTIF
API_URL = "https://3gs21pes.pythonanywhere.com/generate"

def main(page: ft.Page):
    # Setup Layar
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    
    # Warna Tema
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"

    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID Kosong!"
            page.update()
            return

        # UI Loading (Biar user tau lagi loading)
        btn_generate.text = "⏳ MENGHUBUNGI SERVER..."
        btn_generate.disabled = True
        page.update()
        
        try:
            # === KIRIM HWID KE SERVER ===
            # Timeout 10 detik biar gak nunggu kelamaan kalau sinyal jelek
            response = requests.post(API_URL, json={"hwid": txt_hwid.value}, timeout=10)
            
            # BACA JAWABAN SERVER
            data = response.json()
            
            if data['status'] == 'sukses':
                txt_result.value = data['license']
                page.show_snack_bar(ft.SnackBar(content=ft.Text("Sukses Dibuat!"), bgcolor="green"))
            else:
                txt_result.value = f"Error: {data.get('pesan')}"
                
        except Exception as err:
            txt_result.value = "Gagal Koneksi Server!"
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Cek Internet Anda!"), bgcolor="red"))

        # Reset UI
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        page.update()

    async def paste_click(e):
        clip = await page.get_clipboard()
        if clip:
            # Kita bersihkan spasi juga di HP biar rapi
            txt_hwid.value = "".join(clip.split()) 
            page.update()

    def copy_click(e):
        if txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Disalin!")))

    # --- UI ---
    txt_hwid = ft.TextField(label="HWID", text_align=ft.TextAlign.CENTER, border_color=NEON_GREEN)
    txt_result = ft.TextField(label="Lisensi", read_only=True, text_align=ft.TextAlign.CENTER, border_color=BLUE_BTN)
    btn_generate = ft.ElevatedButton("GENERATE LISENSI", on_click=generate_click, bgcolor=BLUE_BTN, color="black")

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
