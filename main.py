import flet as ft
import requests
import asyncio

# --- URL SERVER FIX (JANGAN DIUBAH) ---
# Pastikan tidak ada spasi di awal/akhir string
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

    # --- FUNGSI GENERATE LISENSI ---
    async def generate_click(e):
        if not txt_hwid.value:
            txt_hwid.error_text = "HWID Kosong!"
            page.update()
            return

        # UI Loading
        btn_generate.text = "⏳ MENGHUBUNGI SERVER..."
        btn_generate.disabled = True
        txt_result.value = "Sedang menghubungkan..."
        page.update()
        
        try:
            # Kirim Data ke Server
            # verify=False untuk melewati masalah SSL di beberapa HP
            response = requests.post(
                API_URL, 
                json={"hwid": txt_hwid.value}, 
                timeout=20, # Waktu tunggu lebih lama (20 detik)
                verify=False 
            )
            
            # Cek Jawaban Server
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'sukses':
                    txt_result.value = data['license']
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Sukses!"), bgcolor="green"))
                else:
                    txt_result.value = f"Gagal: {data.get('pesan')}"
            else:
                txt_result.value = f"Error Server: {response.status_code}"
                
        except Exception as err:
            # Tampilkan Error Lengkap biar ketahuan kenapa
            txt_result.value = f"Koneksi Gagal:\n{str(err)}"
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Cek Internet / URL"), bgcolor="red"))

        # Reset Tombol
        btn_generate.text = "GENERATE LISENSI"
        btn_generate.disabled = False
        page.update()

    # --- FUNGSI TEMPEL (PASTE) YANG DIPERBAIKI ---
    async def paste_click(e):
        try:
            # Mengambil teks dari clipboard HP
            clip_text = await page.get_clipboard_async()
            
            if clip_text:
                # Bersihkan spasi/enter yang ikut tercopy
                clean_text = "".join(clip_text.split())
                txt_hwid.value = clean_text
                txt_hwid.error_text = None
                page.show_snack_bar(ft.SnackBar(content=ft.Text("HWID Ditempel!")))
            else:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("Clipboard Kosong!"), bgcolor="orange"))
        except Exception as err:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Gagal Tempel: {str(err)}"), bgcolor="red"))
        
        page.update()

    # --- FUNGSI SALIN (COPY) ---
    def copy_click(e):
        if txt_result.value and "Koneksi" not in txt_result.value:
            page.set_clipboard(txt_result.value)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Disalin!")))
        else:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Belum ada lisensi!"), bgcolor="orange"))

    # --- KOMPONEN UI ---
    txt_hwid = ft.TextField(
        label="HWID Pengguna", 
        text_align=ft.TextAlign.CENTER, 
        border_color=NEON_GREEN
    )
    
    txt_result = ft.TextField(
        label="Hasil Lisensi", 
        read_only=True, 
        multiline=True, # Agar pesan error panjang bisa terbaca
        text_align=ft.TextAlign.CENTER, 
        border_color=BLUE_BTN,
        text_size=12
    )

    btn_generate = ft.ElevatedButton(
        "GENERATE LISENSI", 
        on_click=generate_click, 
        bgcolor=BLUE_BTN, 
        color="black",
        width=200
    )

    # --- SUSUN LAYOUT ---
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
