import flet as ft
import json

def main(page: ft.Page):
    page.title = "Recherche de Plats"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.colors.with_opacity(0.95, "#667eea")
    
    # Configuration pour mobile
    page.window_width = 400
    page.window_height = 800
    
    # Stockage de l'historique (max 5 éléments)
    history_list = []
    
    # Charger l'historique du stockage local si disponible
    def load_history():
        try:
            stored = page.client_storage.get("dish_history")
            if stored:
                return json.loads(stored)[:5]
        except:
            pass
        return []
    
    def save_history():
        try:
            page.client_storage.set("dish_history", json.dumps(history_list[:5]))
        except:
            pass
    
    history_list = load_history()
    
    # --- COMPOSANTS UI ---
    title = ft.Text(
        "🍽️ Recherche de Plats",
        size=32,
        weight=ft.FontWeight.W_600,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )
    
    # Image principale affichée
    
    # Placeholder quand l'image n'existe pas
    image_placeholder = ft.Container(
        content=ft.Column([
            ft.Icon(ft.icons.RESTAURANT, size=80, color=ft.colors.with_opacity(0.3, ft.colors.WHITE)),
            ft.Text(
                "Image introuvable",
                size=18,
                color=ft.colors.with_opacity(0.7, ft.colors.WHITE),
                weight=ft.FontWeight.W_500
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
           alignment=ft.MainAxisAlignment.CENTER,
           spacing=10),
        width=300,
        height=300,
        border_radius=15,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE)
    )
    
    main_image = ft.Image(
        src="",
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        border_radius=15,
        visible=False,
        error_content=image_placeholder
    )
    
    dish_name_display = ft.Text(
        "",
        size=24,
        weight=ft.FontWeight.W_600,
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        visible=False
    )
    
    error_txt = ft.Text(
        color=ft.colors.RED_400,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        visible=False
    )
    
    history_card = ft.Card(
        content=ft.Container(
            content=ft.Column(spacing=10),
            padding=20,
            border_radius=20,
        ),
        elevation=5,
        visible=False
    )

    def show_error(message):
        error_txt.value = message
        error_txt.visible = True
        main_image.visible = False
        dish_name_display.visible = False
        page.update()
        
        # Auto-hide après 3 secondes
        import threading
        def hide():
            import time
            time.sleep(3)
            error_txt.visible = False
            page.update()
        threading.Thread(target=hide, daemon=True).start()

    def add_to_history(dish_code):
        # Retirer si déjà présent
        if dish_code in history_list:
            history_list.remove(dish_code)
        # Ajouter au début
        history_list.insert(0, dish_code)
        # Garder seulement les 5 derniers
        while len(history_list) > 5:
            history_list.pop()
        save_history()
        render_history()

    def render_history():
        history_column = history_card.content.content
        history_column.controls.clear()
        
        if history_list:
            # En-tête
            header = ft.Row([
                ft.Text("Historique de recherche", size=20, weight=ft.FontWeight.W_600),
                ft.ElevatedButton(
                    "Effacer",
                    icon=ft.icons.DELETE_SWEEP,
                    on_click=clear_all,
                    bgcolor=ft.colors.RED_400,
                    color=ft.colors.WHITE,
                    height=35
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            history_column.controls.append(header)
            
            # Liste d'historique avec miniatures
            for item in history_list:
                history_item = ft.Container(
                    content=ft.Row([
                        ft.Image(
                            src=f"{item}.png",
                            width=50,
                            height=50,
                            fit=ft.ImageFit.COVER,
                            border_radius=8
                        ),
                        ft.Text(item, size=18, weight=ft.FontWeight.W_600),
                    ], spacing=15),
                    padding=12,
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                    border_radius=12,
                    on_click=lambda e, code=item: search_dish(code),
                    ink=True
                )
                history_column.controls.append(history_item)
            
            history_card.visible = True
        else:
            history_card.visible = False
        
        page.update()

    def search_dish(dish_code=None):
        # Récupérer le code depuis l'input ou le paramètre
        code = dish_code if dish_code else txt_input.value.strip()
        
        if not code:
            show_error("Veuillez entrer un code de plat")
            return
        
        # Convertir en majuscules pour uniformiser
        code = code.upper()
        
        # Construire le chemin de l'image
        # Flet cherchera automatiquement dans assets_dir
        image_path = f"{code}.png"
        
        # Afficher l'image (si elle n'existe pas, error_content s'affichera)
        main_image.src = image_path
        main_image.visible = True
        dish_name_display.value = f"Plat {code}"
        dish_name_display.visible = True
        error_txt.visible = False
        
        # Ajouter à l'historique
        add_to_history(code)
        
        # Vider l'input si c'est une nouvelle recherche
        if not dish_code:
            txt_input.value = ""
        
        page.update()

    def clear_all(e):
        history_list.clear()
        save_history()
        render_history()
        main_image.visible = False
        dish_name_display.visible = False
        page.update()

    txt_input = ft.TextField(
        hint_text="Code du plat (ex: 1A, 2B...)",
        on_submit=lambda e: search_dish(),
        width=300,
        border_radius=50,
        filled=True,
        bgcolor=ft.colors.WHITE,
        border_color=ft.colors.TRANSPARENT,
        focused_border_color="#764ba2",
        focused_border_width=2,
        text_size=18,
        height=60,
        content_padding=ft.padding.only(left=20, right=60, top=10, bottom=10),
        text_align=ft.TextAlign.LEFT,
        autofocus=True,
        cursor_color="#764ba2"
    )

    search_btn = ft.Container(
        content=ft.Icon(ft.icons.SEARCH, color=ft.colors.WHITE, size=22),
        width=44,
        height=44,
        bgcolor="#764ba2",
        border_radius=22,
        on_click=lambda e: search_dish(),
        ink=True
    )

    search_box = ft.Stack([
        txt_input,
        ft.Container(
            content=search_btn,
            right=8,
            top=8
        )
    ], width=300, height=60)

    # --- MISE EN PAGE ---
    page.add(
        ft.Column([
            ft.Container(height=20),
            title,
            ft.Container(height=30),
            search_box,
            ft.Container(height=20),
            error_txt,
            ft.Container(height=20),
            dish_name_display,
            ft.Container(height=10),
            main_image,
            ft.Container(height=30),
            history_card,
            ft.Container(height=40),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
    )
    
    # Charger l'historique au démarrage
    render_history()

# Point d'entrée
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    ft.app(
        target=main, 
        view=ft.AppView.WEB_BROWSER, 
        assets_dir="assets",
        port=port,
        host="0.0.0.0"
    )