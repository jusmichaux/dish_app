import flet as ft
import json

def main(page: ft.Page):
    page.title = "Recherche de Plats"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.bgcolor = ft.Colors.with_opacity(0.95, "#667eea")
    
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
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )
    
    # Grille d'images de résultats
    results_grid = ft.GridView(
        expand=False,
        runs_count=2,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=15,
        run_spacing=15,
        visible=False
    )
    
    loading_indicator = ft.ProgressRing(visible=False, color=ft.Colors.WHITE)
    
    error_txt = ft.Text(
        color=ft.Colors.RED_400,
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
    
    results_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Résultats", size=20, weight=ft.FontWeight.W_600, color=ft.Colors.with_opacity(0.8, ft.Colors.BLACK)),
                loading_indicator,
                results_grid
            ], spacing=15),
            padding=20,
            border_radius=20,
        ),
        elevation=5,
        visible=False
    )

    def show_error(message):
        error_txt.value = message
        error_txt.visible = True
        page.update()
        # Auto-hide après 3 secondes
        import threading
        def hide():
            import time
            time.sleep(3)
            error_txt.visible = False
            page.update()
        threading.Thread(target=hide, daemon=True).start()

    def add_to_history(dish_name):
        # Retirer si déjà présent
        if dish_name in history_list:
            history_list.remove(dish_name)
        # Ajouter au début
        history_list.insert(0, dish_name)
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
                ft.Text("Historique", size=20, weight=ft.FontWeight.W_600),
                ft.ElevatedButton(
                    "Effacer",
                    icon=ft.Icons.DELETE_SWEEP,
                    on_click=clear_all,
                    bgcolor=ft.Colors.RED_400,
                    color=ft.Colors.WHITE,
                    height=35
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            history_column.controls.append(header)
            
            # Liste d'historique
            for item in history_list:
                history_item = ft.Container(
                    content=ft.Row([
                        ft.Container(
                            width=8,
                            height=8,
                            bgcolor="#667eea",
                            border_radius=4
                        ),
                        ft.Text(item, size=15, weight=ft.FontWeight.W_500)
                    ], spacing=10),
                    padding=10,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK),
                    border_radius=12,
                    on_click=lambda e, name=item: search_dish(name),
                    ink=True
                )
                history_column.controls.append(history_item)
            
            history_card.visible = True
        else:
            history_card.visible = False
        
        page.update()

    async def search_dish(dish_name=None):
        query = dish_name if dish_name else txt_input.value.strip()
        if not query:
            show_error("Veuillez entrer un nom de plat")
            return
        
        # Afficher le chargement
        results_card.visible = True
        loading_indicator.visible = True
        results_grid.visible = False
        results_grid.controls.clear()
        page.update()
        
        try:
            # Recherche via API
            import urllib.request
            import json
            
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={urllib.parse.quote(query)}"
            
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            loading_indicator.visible = False
            
            if data.get("meals"):
                meals = data["meals"]
                add_to_history(query)
                
                # Créer les cartes d'images
                for meal in meals:
                    result_item = ft.Container(
                        content=ft.Column([
                            ft.Image(
                                src=meal["strMealThumb"],
                                width=150,
                                height=150,
                                fit=ft.ImageFit.COVER,
                                border_radius=15
                            ),
                            ft.Container(
                                content=ft.Text(
                                    meal["strMeal"],
                                    size=13,
                                    weight=ft.FontWeight.W_500,
                                    text_align=ft.TextAlign.CENTER,
                                    max_lines=2,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                padding=10
                            )
                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            offset=ft.Offset(0, 5)
                        ),
                        ink=True
                    )
                    results_grid.controls.append(result_item)
                
                results_grid.visible = True
                
                if not dish_name:
                    txt_input.value = ""
            else:
                show_error("Aucun plat trouvé. Essayez une autre recherche.")
            
            page.update()
            
        except Exception as e:
            loading_indicator.visible = False
            show_error(f"Erreur de connexion: {str(e)}")
            page.update()

    def clear_all(e):
        history_list.clear()
        save_history()
        render_history()

    txt_input = ft.TextField(
        label="Rechercher un plat...",
        on_submit=lambda _: search_dish(),
        width=300,
        border_radius=50,
        filled=True,
        bgcolor=ft.Colors.WHITE,
        border_color=ft.Colors.TRANSPARENT,
        focused_border_color=ft.Colors.TRANSPARENT,
        text_size=16,
        height=55,
        content_padding=ft.padding.symmetric(horizontal=20, vertical=15)
    )

    search_btn = ft.Container(
        content=ft.Icon(ft.Icons.SEARCH, color=ft.Colors.WHITE, size=20),
        width=40,
        height=40,
        bgcolor="#764ba2",
        border_radius=20,
        alignment=ft.alignment.center,
        on_click=lambda _: search_dish(),
        ink=True
    )

    search_box = ft.Stack([
        txt_input,
        ft.Container(
            content=search_btn,
            right=8,
            top=8
        )
    ], width=300, height=55)

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
            history_card,
            ft.Container(height=20),
            results_card,
            ft.Container(height=40),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0)
    )
    
    # Charger l'historique au démarrage
    render_history()

# Point d'entrée
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, assets_dir="assets")