bl_info = {
    "name": "Accessibility Wheel",
    "author": "ABBAR Loubna, L'ENTETÉ Mary-Kate, AUDOUBERT Lucas",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D View",
    "description": "Roue radiale accessible (navigation clavier, haut contraste)",
    "category": "3D View",
}

import importlib

from . import accessibility_wheel

def register():
    importlib.reload(accessibility_wheel)
    if hasattr(accessibility_wheel, "register"):
        accessibility_wheel.register()

def unregister():
    if hasattr(accessibility_wheel, "unregister"):
        accessibility_wheel.unregister()
