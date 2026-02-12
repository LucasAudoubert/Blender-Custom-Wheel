import bpy

# --- 1. STRUCTURE DE DONNÉES AMÉLIORÉE ---
class CustomToolItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Nom", default="NOM DE L'OUTIL")
    operator: bpy.props.StringProperty(name="ID", default="wm.search_menu")
    color_icon: bpy.props.EnumProperty(
        name="Couleur",
        items=[
            ('COLORSET_01_VEC', "Rouge", "", 'COLORSET_01_VEC', 0),
            ('COLORSET_02_VEC', "Orange", "", 'COLORSET_02_VEC', 1),
            ('COLORSET_03_VEC', "Vert", "", 'COLORSET_03_VEC', 2),
            ('COLORSET_04_VEC', "Bleu", "", 'COLORSET_04_VEC', 3),
            ('COLORSET_05_VEC', "Jaune", "", 'COLORSET_05_VEC', 4),
            ('COLORSET_06_VEC', "Violet", "", 'COLORSET_06_VEC', 5),
            ('COLORSET_07_VEC', "Rose", "", 'COLORSET_07_VEC', 6),
            ('COLORSET_08_VEC', "Cyan", "", 'COLORSET_08_VEC', 7),
            ('COLORSET_09_VEC', "Vert clair", "", 'COLORSET_09_VEC', 8),
            ('COLORSET_10_VEC', "Bleu marine", "", 'COLORSET_10_VEC', 9),
        ],
        default='COLORSET_04_VEC'
    )
    icon_type: bpy.props.EnumProperty(
        name="Icône",
        items=[
            ('NONE', "Aucun", "Pas d'icône"),
            ('OBJECT_DATAMODE', "Objet", "", 'OBJECT_DATAMODE', 0),
            ('MESH_DATA', "Mesh", "", 'MESH_DATA', 1),
            ('MODIFIER', "Modificateur", "", 'MODIFIER', 2),
            ('SHADING_RENDERED', "Matériau", "", 'SHADING_RENDERED', 3),
            ('LIGHT', "Lumière", "", 'LIGHT', 4),
            ('CAMERA_DATA', "Caméra", "", 'CAMERA_DATA', 5),
            ('MOD_ARRAY', "Array", "", 'MOD_ARRAY', 6),
            ('MOD_BEVEL', "Biseau", "", 'MOD_BEVEL', 7),
            ('MOD_SOLIDIFY', "Solidify", "", 'MOD_SOLIDIFY', 8),
            ('MOD_SUBSURF', "Subdivision", "", 'MOD_SUBSURF', 9),
            ('BRUSH_SCULPT', "Sculpt", "", 'BRUSH_SCULPT', 10),
            ('UV', "UV", "", 'UV', 11),
            ('ANIM', "Animation", "", 'ANIM', 12),
        ],
        default='NONE'
    )

# --- 2. MENU DE SÉLECTION D'OUTILS ÉTENDU ---
class PIE_MT_ToolLibrary(bpy.types.Menu):
    bl_label = "Bibliothèque d'Outils"
    bl_idname = "PIE_MT_tool_library"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Barre de recherche
        row = layout.row()
        row.prop(scene, "tool_search", text="", icon='VIEWZOOM')
        row.operator("pie.clear_search", text="", icon='X')
        
        layout.separator()
        
        # Filtrer les outils selon la recherche
        search_text = scene.tool_search.lower() if hasattr(scene, "tool_search") else ""
        
        # Catégorie : PRIMITIVES
        if not search_text or any(term in name.lower() for name in ["primitives", "objets", "mesh"] for term in [search_text]):
            layout.label(text="--- PRIMITIVES ---")
            self.add_op(layout, "Cube", "mesh.primitive_cube_add", 'MESH_CUBE', search_text)
            self.add_op(layout, "Sphère", "mesh.primitive_uv_sphere_add", 'MESH_UVSPHERE', search_text)
            self.add_op(layout, "Cylindre", "mesh.primitive_cylinder_add", 'MESH_CYLINDER', search_text)
            self.add_op(layout, "Cône", "mesh.primitive_cone_add", 'MESH_CONE', search_text)
            self.add_op(layout, "Plan", "mesh.primitive_plane_add", 'MESH_PLANE', search_text)
            self.add_op(layout, "Tore", "mesh.primitive_torus_add", 'MESH_TORUS', search_text)
            self.add_op(layout, "Suzanne", "mesh.primitive_monkey_add", 'MESH_MONKEY', search_text)
            layout.separator()
        
        # Catégorie : MODIFICATEURS
        if not search_text or any(term in name.lower() for name in ["modifiers", "modificateurs"] for term in [search_text]):
            layout.label(text="--- MODIFICATEURS ---")
            self.add_modifier_op(layout, "Biseau", 'BEVEL', 'MOD_BEVEL', search_text)
            self.add_modifier_op(layout, "Subdivision", 'SUBSURF', 'MOD_SUBSURF', search_text)
            self.add_modifier_op(layout, "Array", 'ARRAY', 'MOD_ARRAY', search_text)
            self.add_modifier_op(layout, "Mirroir", 'MIRROR', 'MOD_MIRROR', search_text)
            self.add_modifier_op(layout, "Solidify", 'SOLIDIFY', 'MOD_SOLIDIFY', search_text)
            self.add_modifier_op(layout, "Wireframe", 'WIREFRAME', 'MOD_WIREFRAME', search_text)
            self.add_modifier_op(layout, "Displace", 'DISPLACE', 'MOD_DISPLACE', search_text)
            layout.separator()
        
        # Catégorie : TRANSFORMATIONS
        if not search_text or any(term in name.lower() for name in ["transformer", "déplacer", "rotation", "échelle"] for term in [search_text]):
            layout.label(text="--- TRANSFORMATIONS ---")
            self.add_op(layout, "Déplacer", "transform.translate", 'ORIENTATION_GLOBAL', search_text)
            self.add_op(layout, "Tourner", "transform.rotate", 'ORIENTATION_GLOBAL', search_text)
            self.add_op(layout, "Mettre à l'échelle", "transform.resize", 'ORIENTATION_GLOBAL', search_text)
            layout.separator()
        
        # Catégorie : SHADING
        if not search_text or any(term in name.lower() for name in ["shading", "lissage", "ombrage"] for term in [search_text]):
            layout.label(text="--- SHADING ---")
            self.add_op(layout, "Lissage", "object.shade_smooth", 'SHADING_SMOOTH', search_text)
            self.add_op(layout, "Facettes", "object.shade_flat", 'SHADING_FLAT', search_text)
            self.add_op(layout, "Matériau nouveau", "material.new", 'MATERIAL', search_text)
            layout.separator()
        
        # Catégorie : OBJETS
        if not search_text or any(term in name.lower() for name in ["objets", "lumière", "caméra", "vide"] for term in [search_text]):
            layout.label(text="--- OBJETS ---")
            self.add_light_op(layout, "Point", 'POINT', 'LIGHT_POINT', search_text)
            self.add_light_op(layout, "Soleil", 'SUN', 'LIGHT_SUN', search_text)
            self.add_light_op(layout, "Spot", 'SPOT', 'LIGHT_SPOT', search_text)
            self.add_light_op(layout, "Aire", 'AREA', 'LIGHT_AREA', search_text)
            self.add_op(layout, "Caméra", "object.camera_add", 'CAMERA_DATA', search_text)
            self.add_op(layout, "Vide", "object.empty_add", 'EMPTY_DATA', search_text)
            layout.separator()
        
        # Catégorie : ÉDITION
        if not search_text or any(term in name.lower() for name in ["edit", "éditer", "modifier"] for term in [search_text]):
            layout.label(text="--- ÉDITION ---")
            self.add_op(layout, "Extrusion", "mesh.extrude_region_move", 'FULLSCREEN_EXIT', search_text)
            self.add_op(layout, "Inset", "mesh.inset", 'FULLSCREEN_EXIT', search_text)
            self.add_op(layout, "Bevel", "mesh.bevel", 'MOD_BEVEL', search_text)
            layout.separator()
        
        # Catégorie : SCULPT
        if not search_text or any(term in name.lower() for name in ["sculpt", "peinture"] for term in [search_text]):
            layout.label(text="--- SCULPT ---")
            self.add_op(layout, "Sculpt Draw", "paint.brush_select", 'BRUSH_SCULPT_DRAW', search_text)
            self.add_op(layout, "Sculpt Clay", "paint.brush_select", 'BRUSH_CLAY', search_text)
            layout.separator()
        
        # Catégorie : GESTION
        if not search_text or any(term in name.lower() for name in ["gérer", "supprimer", "dupliquer"] for term in [search_text]):
            layout.label(text="--- GESTION ---")
            self.add_op(layout, "Dupliquer", "object.duplicate_move", 'DUPLICATE', search_text)
            self.add_op(layout, "Supprimer", "object.delete", 'TRASH', search_text)
            self.add_op(layout, "Joindre", "object.join", 'AUTOMERGE_ON', search_text)
            self.add_op(layout, "Séparer", "mesh.separate", 'AUTOMERGE_OFF', search_text)

    def add_op(self, layout, name, op_id, icon, search_text):
        """Ajoute un opérateur standard"""
        if search_text and search_text not in name.lower():
            return
            
        op = layout.operator("pie.add_specific_tool", text=name, icon=icon)
        op.name = name
        op.operator_id = op_id

    def add_modifier_op(self, layout, name, mod_type, icon, search_text):
        """Ajoute un opérateur de modificateur"""
        if search_text and search_text not in name.lower():
            return
            
        op = layout.operator("pie.add_modifier_tool", text=name, icon=icon)
        op.name = name
        op.modifier_type = mod_type

    def add_light_op(self, layout, name, light_type, icon, search_text):
        """Ajoute un opérateur de lumière"""
        if search_text and search_text not in name.lower():
            return
            
        op = layout.operator("pie.add_light_tool", text=name, icon=icon)
        op.name = name
        op.light_type = light_type

# --- 3. LA ROUE (PIE MENU) AMÉLIORÉE ---
class VIEW3D_MT_CustomPie(bpy.types.Menu):
    bl_label = "Roue d'Accessibilité"
    bl_idname = "VIEW3D_MT_custom_pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        scene = context.scene
        
        if len(scene.custom_pie_tools) == 0:
            pie.label(text="Ajoutez des outils", icon='INFO')
            return
        
        # Positionner les outils dans les 8 positions du pie menu
        positions = [
            ('LEFT', 0), ('RIGHT', 1), ('BOTTOM', 2), ('TOP', 3),
            ('TOP_LEFT', 4), ('TOP_RIGHT', 5), ('BOTTOM_LEFT', 6), ('BOTTOM_RIGHT', 7)
        ]
        
        # Diviser en 2 colonnes si plus de 8 outils
        if len(scene.custom_pie_tools) > 8:
            col1 = pie.column()
            col2 = pie.column()
            
            half = len(scene.custom_pie_tools) // 2
            for i, item in enumerate(scene.custom_pie_tools):
                col = col1 if i < half else col2
                self.draw_tool_item(col, item)
        else:
            # Utiliser les positions standards du pie menu
            for i, item in enumerate(scene.custom_pie_tools):
                if i < 8:  # Max 8 positions dans un pie menu
                    icon = item.icon_type if item.icon_type != 'NONE' else item.color_icon
                    try:
                        pie.operator(item.operator, text=item.name, icon=icon)
                    except:
                        pie.label(text=f"{item.name}", icon='ERROR')

    def draw_tool_item(self, layout, item):
        """Dessine un item d'outil avec son icône personnalisée"""
        row = layout.row(align=True)
        
        # Utiliser l'icône personnalisée si définie
        icon = item.icon_type if item.icon_type != 'NONE' else item.color_icon
        
        try:
            row.operator(item.operator, text=item.name, icon=icon)
        except:
            row.label(text=f"{item.name}", icon='ERROR')

# --- 4. PANNEAU CONFIG AMÉLIORÉ ---
class UI_PT_AccessibilityConfig(bpy.types.Panel):
    bl_label = "Configuration Accessibilité"
    bl_idname = "UI_PT_accessibility_config"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Accessibilité'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Section : Contrôles rapides
        box = layout.box()
        box.label(text="Contrôles Rapides", icon='TOOL_SETTINGS')
        row = box.row(align=True)
        row.operator("wm.call_menu_pie", text="Ouvrir Roue (Shift+Q)", icon='MENU_PANEL').name = "VIEW3D_MT_custom_pie"
        row.operator("pie.reset_tools", text="", icon='LOOP_BACK')
        
        # Section : Bibliothèque
        box = layout.box()
        box.label(text="Bibliothèque d'Outils", icon='BOOKMARKS')
        box.menu("PIE_MT_tool_library", text="Parcourir la Bibliothèque", icon='ADD')
        
        if hasattr(scene, "tool_search") and scene.tool_search:
            box.label(text=f"Recherche : {scene.tool_search}", icon='VIEWZOOM')
        
        # Section : Outils configurés
        box = layout.box()
        box.label(text="Outils Configurés", icon='TOOL_SETTINGS')
        
        if len(scene.custom_pie_tools) == 0:
            box.label(text="Aucun outil configuré", icon='INFO')
            box.operator("pie.add_default_tools", text="Ajouter outils par défaut", icon='ADD')
        else:
            # Boutons pour réorganiser
            row = box.row(align=True)
            row.operator("pie.move_tool_up", text="", icon='TRIA_UP')
            row.operator("pie.move_tool_down", text="", icon='TRIA_DOWN')
            row.operator("pie.clear_all_tools", text="Tout supprimer", icon='TRASH')
            
            # Liste des outils
            for i, item in enumerate(scene.custom_pie_tools):
                tool_box = box.box()
                header = tool_box.row(align=True)
                header.prop(item, "color_icon", text="", icon_only=True)
                header.prop(item, "name", text="")
                
                # Boutons d'action
                actions = header.row(align=True)
                actions.operator("pie.remove_tool", text="", icon='X').index = i
                
                # Configuration avancée
                config_row = tool_box.row(align=True)
                config_row.prop(item, "operator", text="Opérateur")
                config_row.prop(item, "icon_type", text="Icône")

# --- 5. OPÉRATEURS SUPPLEMENTAIRES ---
class UI_OT_AddSpecificTool(bpy.types.Operator):
    """Ajoute un outil choisi depuis la bibliothèque"""
    bl_idname = "pie.add_specific_tool"
    bl_label = "Ajouter cet outil"
    
    name: bpy.props.StringProperty()
    operator_id: bpy.props.StringProperty()

    def execute(self, context):
        item = context.scene.custom_pie_tools.add()
        item.name = self.name
        item.operator = self.operator_id
        self.report({'INFO'}, f"Outil '{self.name}' ajouté")
        return {'FINISHED'}

class UI_OT_AddModifierTool(bpy.types.Operator):
    """Ajoute un modificateur spécifique"""
    bl_idname = "pie.add_modifier_tool"
    bl_label = "Ajouter modificateur"
    
    name: bpy.props.StringProperty()
    modifier_type: bpy.props.StringProperty()

    def execute(self, context):
        item = context.scene.custom_pie_tools.add()
        item.name = f"Modifier: {self.name}"
        item.operator = f"object.modifier_add(type='{self.modifier_type}')"
        self.report({'INFO'}, f"Modificateur '{self.name}' ajouté")
        return {'FINISHED'}

class UI_OT_AddLightTool(bpy.types.Operator):
    """Ajoute une lumière spécifique"""
    bl_idname = "pie.add_light_tool"
    bl_label = "Ajouter lumière"
    
    name: bpy.props.StringProperty()
    light_type: bpy.props.StringProperty()

    def execute(self, context):
        item = context.scene.custom_pie_tools.add()
        item.name = f"Lumière: {self.name}"
        item.operator = f"object.light_add(type='{self.light_type}')"
        self.report({'INFO'}, f"Lumière '{self.name}' ajouté")
        return {'FINISHED'}

class UI_OT_RemoveTool(bpy.types.Operator):
    bl_idname = "pie.remove_tool"
    bl_label = "Supprimer"
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        if 0 <= self.index < len(context.scene.custom_pie_tools):
            context.scene.custom_pie_tools.remove(self.index)
            self.report({'INFO'}, "Outil supprimé")
        return {'FINISHED'}

class UI_OT_MoveToolUp(bpy.types.Operator):
    """Déplacer l'outil vers le haut"""
    bl_idname = "pie.move_tool_up"
    bl_label = "Monter"
    
    index: bpy.props.IntProperty(default=0)
    
    def execute(self, context):
        scene = context.scene
        tools = scene.custom_pie_tools
        if self.index > 0 and self.index < len(tools):
            tools.move(self.index, self.index - 1)
        return {'FINISHED'}

class UI_OT_MoveToolDown(bpy.types.Operator):
    """Déplacer l'outil vers le bas"""
    bl_idname = "pie.move_tool_down"
    bl_label = "Descendre"
    
    index: bpy.props.IntProperty(default=0)
    
    def execute(self, context):
        scene = context.scene
        tools = scene.custom_pie_tools
        if self.index >= 0 and self.index < len(tools) - 1:
            tools.move(self.index, self.index + 1)
        return {'FINISHED'}

class UI_OT_ClearAllTools(bpy.types.Operator):
    """Supprimer tous les outils"""
    bl_idname = "pie.clear_all_tools"
    bl_label = "Tout supprimer"
    
    def execute(self, context):
        scene = context.scene
        scene.custom_pie_tools.clear()
        self.report({'INFO'}, "Tous les outils ont été supprimés")
        return {'FINISHED'}

class UI_OT_AddDefaultTools(bpy.types.Operator):
    """Ajouter un ensemble d'outils par défaut"""
    bl_idname = "pie.add_default_tools"
    bl_label = "Ajouter par défaut"
    
    def execute(self, context):
        defaults = [
            ("Cube", "mesh.primitive_cube_add", 'COLORSET_01_VEC', 'MESH_DATA'),
            ("Sphère", "mesh.primitive_uv_sphere_add", 'COLORSET_03_VEC', 'MESH_DATA'),
            ("Déplacer", "transform.translate", 'COLORSET_04_VEC', 'OBJECT_DATAMODE'),
            ("Tourner", "transform.rotate", 'COLORSET_05_VEC', 'OBJECT_DATAMODE'),
            ("Lissage", "object.shade_smooth", 'COLORSET_06_VEC', 'SHADING_RENDERED'),
            ("Supprimer", "object.delete", 'COLORSET_02_VEC', 'NONE'),
            ("Lumière", "object.light_add", 'COLORSET_07_VEC', 'LIGHT'),
            ("Caméra", "object.camera_add", 'COLORSET_08_VEC', 'CAMERA_DATA'),
        ]
        
        for name, op, color, icon in defaults:
            item = context.scene.custom_pie_tools.add()
            item.name = name
            item.operator = op
            item.color_icon = color
            item.icon_type = icon
        
        self.report({'INFO'}, "Outils par défaut ajoutés")
        return {'FINISHED'}

class UI_OT_ResetTools(bpy.types.Operator):
    """Réinitialiser à l'ensemble par défaut"""
    bl_idname = "pie.reset_tools"
    bl_label = "Réinitialiser"
    
    def execute(self, context):
        bpy.ops.pie.clear_all_tools()
        bpy.ops.pie.add_default_tools()
        return {'FINISHED'}

class UI_OT_ClearSearch(bpy.types.Operator):
    """Effacer la recherche"""
    bl_idname = "pie.clear_search"
    bl_label = "Effacer recherche"
    
    def execute(self, context):
        context.scene.tool_search = ""
        return {'FINISHED'}

# --- 6. REGISTER ---
classes = (
    CustomToolItem,
    PIE_MT_ToolLibrary,
    VIEW3D_MT_CustomPie,
    UI_PT_AccessibilityConfig,
    UI_OT_AddSpecificTool,
    UI_OT_AddModifierTool,
    UI_OT_AddLightTool,
    UI_OT_RemoveTool,
    UI_OT_MoveToolUp,
    UI_OT_MoveToolDown,
    UI_OT_ClearAllTools,
    UI_OT_AddDefaultTools,
    UI_OT_ResetTools,
    UI_OT_ClearSearch,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Propriétés de scène
    bpy.types.Scene.custom_pie_tools = bpy.props.CollectionProperty(type=CustomToolItem)
    bpy.types.Scene.tool_search = bpy.props.StringProperty(name="Recherche", default="")
    
    # Configuration des raccourcis clavier
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS', shift=True)
        kmi.properties.name = "VIEW3D_MT_custom_pie"
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    # Supprimer les propriétés
    del bpy.types.Scene.custom_pie_tools
    del bpy.types.Scene.tool_search
    
    # Désenregistrer les classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()