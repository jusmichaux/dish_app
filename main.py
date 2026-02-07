import flet as ft
import json

def main(page: ft.Page):
    page.title = "Recherche de Plats"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = "#FFFFFF"
    
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
    
    # Header avec dégradé
    header = ft.Container(
        content=ft.Column([
            ft.Container(height=20),
            ft.Text(
                "🍽️ Menu Digital",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                "Recherchez votre plat",
                size=14,
                color=ft.colors.with_opacity(0.9, ft.colors.WHITE),
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#667eea", "#764ba2"]
        ),
        border_radius=ft.border_radius.only(bottom_left=30, bottom_right=30),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.colors.with_opacity(0.15, "#667eea"),
            offset=ft.Offset(0, 10)
        )
    )
    
    # Placeholder quand l'image n'existe pas
    image_placeholder = ft.Container(
        content=ft.Column([
            ft.Icon(
                ft.icons.RESTAURANT_MENU_ROUNDED, 
                size=70, 
                color=ft.colors.with_opacity(0.15, "#667eea")
            ),
            ft.Text(
                "Image introuvable",
                size=16,
                color=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                weight=ft.FontWeight.W_500
            ),
            ft.Text(
                "Vérifiez le code",
                size=12,
                color=ft.colors.with_opacity(0.3, ft.colors.BLACK)
            )
        ], 
           horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
           alignment=ft.MainAxisAlignment.CENTER,
           spacing=8),
        width=320,
        height=320,
        border_radius=20,
        bgcolor=ft.colors.with_opacity(0.03, ft.colors.BLACK),
        border=ft.border.all(2, ft.colors.with_opacity(0.1, "#667eea"))
    )
    
    # Image principale avec ombre
    main_image = ft.Container(
        content=ft.Image(
            src="",
            width=320,
            height=320,
            fit=ft.ImageFit.CONTAIN,
            border_radius=20,
            error_content=image_placeholder
        ),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=30,
            color=ft.colors.with_opacity(0.12, ft.colors.BLACK),
            offset=ft.Offset(0, 10)
        ),
        visible=False
    )
    
    # Nom du plat avec badge moderne
    dish_name_display = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text(
                    "",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#667eea"
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
            )
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ft.colors.with_opacity(0.08, "#667eea"),
        border_radius=25,
        border=ft.border.all(2, ft.colors.with_opacity(0.2, "#667eea")),
        visible=False
    )
    
    error_txt = ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED_400, size=20),
            ft.Text(
                "",
                color=ft.colors.RED_400,
                weight=ft.FontWeight.W_500,
                size=14
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.RED_400),
        border_radius=15,
        padding=15,
        visible=False
    )

    def show_error(message):
        error_txt.content.controls[1].value = message
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
        if dish_code in history_list:
            history_list.remove(dish_code)
        history_list.insert(0, dish_code)
        while len(history_list) > 5:
            history_list.pop()
        save_history()
        render_history()

    # Card d'historique moderne
    history_card = ft.Container(
        content=ft.Column(spacing=12),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=25,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=20,
            color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
            offset=ft.Offset(0, 5)
        ),
        border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.BLACK)),
        visible=False
    )

    def render_history():
        history_column = history_card.content
        history_column.controls.clear()
        
        if history_list:
            # En-tête moderne
            header_row = ft.Row([
                ft.Row([
                    ft.Icon(ft.icons.HISTORY, color="#667eea", size=22),
                    ft.Text(
                        "Historique", 
                        size=18, 
                        weight=ft.FontWeight.BOLD,
                        color="#2D3748"
                    )
                ], spacing=8),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.DELETE_SWEEP, color=ft.colors.WHITE, size=18),
                        ft.Text("Effacer", color=ft.colors.WHITE, size=13, weight=ft.FontWeight.W_500)
                    ], spacing=5),
                    bgcolor=ft.colors.RED_400,
                    border_radius=20,
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    on_click=clear_all,
                    ink=True
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            history_column.controls.append(header_row)
            
            history_column.controls.append(ft.Container(height=5))
            
            # Liste d'historique moderne
            for item in history_list:
                history_item = ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Image(
                                src=f"{item}.png",
                                width=55,
                                height=55,
                                fit=ft.ImageFit.COVER,
                                border_radius=12
                            ),
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=8,
                                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                                offset=ft.Offset(0, 2)
                            )
                        ),
                        ft.Column([
                            ft.Text(
                                f"Plat {item}", 
                                size=16, 
                                weight=ft.FontWeight.BOLD,
                                color="#2D3748"
                            ),
                            ft.Text(
                                "Cliquer pour afficher", 
                                size=12, 
                                color=ft.colors.with_opacity(0.5, ft.colors.BLACK)
                            )
                        ], spacing=2),
                        ft.Icon(ft.icons.CHEVRON_RIGHT, color="#667eea", size=20)
                    ], spacing=15, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=12,
                    bgcolor=ft.colors.with_opacity(0.03, "#667eea"),
                    border_radius=15,
                    border=ft.border.all(1, ft.colors.with_opacity(0.1, "#667eea")),
                    on_click=lambda e, code=item: search_dish(code),
                    ink=True,
                    animate=ft.animation.Animation(300, "easeOut")
                )
                history_column.controls.append(history_item)
            
            history_card.visible = True
        else:
            history_card.visible = False
        
        page.update()

    def search_dish(dish_code=None):
        code = dish_code if dish_code else txt_input.value.strip()
        
        if not code:
            show_error("Veuillez entrer un code de plat")
            return
        
        code = code.upper()
        image_path = f"{code}.png"
        
        # Afficher l'image
        main_image.content.src = image_path
        main_image.visible = True
        dish_name_display.content.controls[0].content.value = f"Plat {code}"
        dish_name_display.visible = True
        error_txt.visible = False
        
        add_to_history(code)
        
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

    # Input moderne avec ombre
    txt_input = ft.TextField(
        hint_text="Ex: 1A, 2B, 10C...",
        hint_style=ft.TextStyle(
            size=16,
            color=ft.colors.with_opacity(0.4, ft.colors.BLACK)
        ),
        on_submit=lambda e: search_dish(),
        width=320,
        border_radius=25,
        filled=True,
        bgcolor=ft.colors.WHITE,
        border_color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
        focused_border_color="#667eea",
        focused_border_width=2,
        text_size=18,
        height=60,
        content_padding=ft.padding.only(left=25, right=70, top=10, bottom=10),
        text_align=ft.TextAlign.LEFT,
        autofocus=True,
        cursor_color="#667eea",
        color="#2D3748"
    )

    # Bouton de recherche moderne
    search_btn = ft.Container(
        content=ft.Icon(ft.icons.SEARCH_ROUNDED, color=ft.colors.WHITE, size=24),
        width=48,
        height=48,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#667eea", "#764ba2"]
        ),
        border_radius=24,
        on_click=lambda e: search_dish(),
        ink=True,
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.colors.with_opacity(0.3, "#667eea"),
            offset=ft.Offset(0, 5)
        )
    )

    # Container de recherche avec ombre
    search_container = ft.Container(
        content=ft.Stack([
            txt_input,
            ft.Container(
                content=search_btn,
                right=6,
                top=6
            )
        ], width=320, height=60),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=25,
            color=ft.colors.with_opacity(0.08, ft.colors.BLACK),
            offset=ft.Offset(0, 8)
        ),
        border_radius=25
    )

    # --- MISE EN PAGE ---
    page.add(
        ft.Column([
            header,
            ft.Container(height=30),
            search_container,
            ft.Container(height=25),
            error_txt,
            ft.Container(height=15),
            dish_name_display,
            ft.Container(height=15),
            main_image,
            ft.Container(height=35),
            ft.Container(
                content=history_card,
                width=360,
                padding=ft.padding.symmetric(horizontal=20)
            ),
            ft.Container(height=40),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
    )
    
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