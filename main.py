import flet as ft
import requests
import asyncio

# Pastikan URL ini benar (sesuai yang Mas tes di browser)
API_URL = "https://3gs21pes.pythonanywhere.com/generate"

def main(page: ft.Page):
    # Setup Layar
    page.title = "PES 21 Keygen"
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    
    NEON_GREEN = "#B9F01D"
    BLUE_BTN = "#00BFFF"

    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID Kosong!"
            page.update()
            return

        # UI Loading
        btn_generate.text = "⏳ MENGHUBUNGI SERVER..."
        btn_generate.disabled = True
        # Bersihkan pesan error sebelumnya
        txt_result.value = "Sedang menghubungkan..." 
        page.update()
        
        try:
            # === PERUBAHAN PENTING DISINI ===
            # verify=False : Biar Android tidak memblokir koneksi SSL/HTTPS
            # timeout=15   : Kasih waktu lebih lama (15 detik)
            response = requests.post(
                API_URL, 
                json={"hwid": txt_hwid.value}, 
                timeout=15, 
                verify=False
            )
            
            # Cek status kode (200 artinya OK)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'sukses':
                    txt_result.value = data['license']
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Sukses!"), bgcolor="green"))
                else:
                    txt_result.value = f"Server Menolak: {data.get('pesan')}"
            else:
                txt_result.value = f"Error HTTP: {response.status_code}"
                
        except Exception as err:
            # === TAMPILKAN ERROR ASLI BIAR KITA TAU PENYEBABNYA ===
            error_msg = str(err)
            print(error_msg) # Print ke log
            txt_result.value = f"ERROR TEKNIS:\n{error_msg}"
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Gagal Koneksi"), bgcolor="red"))

        # Reset Tombol
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        page.update()

    async def paste_click(e):
        clip = await page.get_clipboard()
        if clip:
            txt_hwid.value = "".join(clip.split())
            page.update()

    def copy_click(e):
        if txt_result.value and "ERROR" not in txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Disalin!")))

    # --- UI ---
    txt_hwid = ft.TextField(label="HWID", text_align=ft.TextAlign.CENTER, border_color=NEON_GREEN)
    txt_result = ft.TextField(
        label="Hasil Lisensi / Error", 
        read_only=True, 
        multiline=True, # Biar pesan error panjang bisa terbaca
        text_align=ft.TextAlign.CENTER, 
        border_color=BLUE_BTN,
        text_size=12 # Kecilkan dikit biar muat
    )
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
