import bpy

# --- 1. STRUCTURE DE DONNÉES ---
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
        ],
        default='COLORSET_04_VEC'
    )

# --- 2. LE MENU DE SÉLECTION D'OUTILS (BIBLIOTHÈQUE) ---
class PIE_MT_ToolLibrary(bpy.types.Menu):
    bl_label = "Choisir un outil type"

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="--- OBJETS MESH ---")
        self.add_op(layout, "CUBE", "mesh.primitive_cube_add", 'MESH_CUBE')
        self.add_op(layout, "SPHÈRE", "mesh.primitive_uv_sphere_add", 'MESH_UVSPHERE')
        self.add_op(layout, "SINGE", "mesh.primitive_monkey_add", 'MESH_MONKEY')
        
        layout.separator()
        layout.label(text="--- MODIFICATION ---")
        self.add_op(layout, "LISSAGE", "object.shade_smooth", 'SHADERSMOOTH')
        self.add_op(layout, "BISEAU", "object.modifier_add", 'MOD_BEVEL')
        self.add_op(layout, "SUBDIVISION", "object.modifier_add", 'MOD_SUBSURF')

        layout.separator()
        layout.label(text="--- DIVERS ---")
        self.add_op(layout, "LUMIÈRE", "object.light_add", 'LIGHT')
        self.add_op(layout, "CAMÉRA", "object.camera_add", 'CAMERA_DATA')
        self.add_op(layout, "EFFACER", "object.delete", 'TRASH')

    def add_op(self, layout, name, op_id, icon):
        op = layout.operator("pie.add_specific_tool", text=name, icon=icon)
        op.name = name
        op.operator_id = op_id

# --- 3. LA ROUE (PIE MENU) ---
class VIEW3D_MT_CustomPie(bpy.types.Menu):
    bl_label = "Roue Accessibilité"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        scene = context.scene
        
        if len(scene.custom_pie_tools) == 0:
            pie.label(text="LISTE VIDE")
            return

        for item in scene.custom_pie_tools:
            try:
                pie.operator(item.operator, text=item.name.upper(), icon=item.color_icon)
            except:
                pie.label(text=f"ERREUR: {item.name}")

# --- 4. PANNEAU CONFIG (N-PANEL) ---
class UI_PT_AccessibilityConfig(bpy.types.Panel):
    bl_label = "Configuration Accessibilité"
    bl_idname = "UI_PT_accessibility_config"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Accessibilité'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("wm.call_menu_pie", text="OUVRIR LA ROUE (Shift+Q)", icon='MENU_PANEL').name = "VIEW3D_MT_CustomPie"
        layout.separator()

        # LE NOUVEAU MENU DE SÉLECTION RAPIDE
        layout.menu("PIE_MT_ToolLibrary", text="CHOISIR UN OUTIL TYPE", icon='ADD')
        
        layout.separator()

        for i, item in enumerate(scene.custom_pie_tools):
            box = layout.box()
            row = box.row(align=True)
            row.prop(item, "color_icon", text="")
            row.prop(item, "name", text="")
            row.operator("pie.remove_tool", text="", icon='TRASH').index = i
            box.prop(item, "operator", text="ID")

# --- 5. OPÉRATEURS ---
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
        return {'FINISHED'}

class UI_OT_RemoveTool(bpy.types.Operator):
    bl_idname = "pie.remove_tool"
    bl_label = "Supprimer"
    index: bpy.props.IntProperty()
    def execute(self, context):
        context.scene.custom_pie_tools.remove(self.index)
        return {'FINISHED'}

# --- 6. REGISTER ---
classes = (
    CustomToolItem, 
    PIE_MT_ToolLibrary,
    VIEW3D_MT_CustomPie, 
    UI_PT_AccessibilityConfig, 
    UI_OT_AddSpecificTool, 
    UI_OT_RemoveTool
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.custom_pie_tools = bpy.props.CollectionProperty(type=CustomToolItem)
    
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS', shift=True)
        kmi.properties.name = "VIEW3D_MT_CustomPie"
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.custom_pie_tools

if __name__ == "__main__":
    register()