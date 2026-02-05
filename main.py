import flet as ft

def main(page: ft.Page):
    page.title = "Sushi Finder"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    # Pour le web, on définit souvent le dossier assets ainsi
    page.assets_dir = "assets"

    history_list = []

    # --- COMPOSANTS UI ---
    title = ft.Text("CHERCHER UN PLAT", size=28, weight="bold", color=ft.Colors.AMBER)
    
    img_display = ft.Image(
        src="", 
        width=250, 
        height=250, 
        fit="contain",
        border_radius=15,
        visible=False
    )
    
    error_txt = ft.Text(color="red", weight="bold", text_align="center")
    history_column = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def delete_from_history(e, item):
        history_list.remove(item)
        render_history()

    def render_history():
        history_column.controls.clear()
        if history_list:
            history_column.controls.append(ft.Text("Dernières recherches", italic=True, color="grey"))
        
        for item in history_list:
            # On s'assure de pointer vers le bon fichier dans assets
            img_path = f"{item}.png"
            history_column.controls.append(
                ft.Container(
                    content=ft.ListTile(
                        leading=ft.Image(src=img_path, width=40, height=40, fit="cover", border_radius=5),
                        title=ft.Text(item, weight="bold"),
                        trailing=ft.IconButton(ft.Icons.DELETE_OUTLINE, on_click=lambda e, i=item: delete_from_history(e, i)),
                        on_click=lambda e, name=item: search_image(name)
                    ),
                    bgcolor=ft.Colors.SURFACE_VARIANT,
                    border_radius=10,
                    width=400
                )
            )
        page.update()

    def search_image(name_to_find=None):
        raw_name = name_to_find if name_to_find else txt_input.value.strip()
        if not raw_name: return
        
        # On force en majuscules pour correspondre à ton exemple "1A"
        name = raw_name.upper()
        full_name = f"{name}.png"
        
        # MISE À JOUR : On utilise le chemin relatif direct
        img_display.src = full_name 
        img_display.visible = True
        error_txt.value = ""
        
        if name not in history_list:
            history_list.insert(0, name)
            if len(history_list) > 10: history_list.pop()
        
        if not name_to_find: txt_input.value = ""
        render_history()
        page.update()

    def clear_all(e):
        history_list.clear()
        img_display.visible = False
        render_history()

    txt_input = ft.TextField(
        label="Code (ex: 1A)",
        on_submit=lambda _: search_image(),
        width=250,
        text_align="center",
        border_radius=15
    )

    # --- MISE EN PAGE ---
    page.add(
        ft.Column([
            title,
            ft.Container(height=10), # Remplace VerticalDivider
            txt_input,
            ft.ElevatedButton("Rechercher", icon=ft.Icons.SEARCH, on_click=lambda _: search_image(), width=200),
            error_txt,
            ft.Container(height=20),
            img_display,
            ft.Divider(height=40),
            ft.Row([
                ft.Text("Historique", size=20, weight="bold"),
                ft.TextButton("Tout effacer", on_click=clear_all, color="red")
            ], alignment="spaceBetween", width=400),
            history_column
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

# Utilisation de la nouvelle syntaxe recommandée
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
