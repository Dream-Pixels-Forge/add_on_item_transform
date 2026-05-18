"""
Internationalization (i18n) module - Translation support for Item Transform Pro.

Uses Blender's built-in translation system via bpy.app.translations.
Provides a simple pgettext wrapper for use across all modules.

Usage in other modules:
    from .i18n import iface_ as _
    label = _("My Label")

To add a new language:
    1. Add a new entry to TRANSLATIONS dict with the locale code
    2. Provide translations for all message IDs
"""

import bpy

# Translation context for this addon (matches __package__)
TRANSLATION_CONTEXT = "item_transform"

# ============================================================
# Translation Dictionary
# Format: {locale: {(context, msg_id): translation}}
# ============================================================

TRANSLATIONS = {
    "fr_FR": {
        # -- Main Panel --
        ("*", "Item Transform Pro"): "Item Transform Pro",
        ("*", "Professional Transform Toolkit"): "Boite a Outils de Transformation",
        ("*", "Quick Transform"): "Transformation Rapide",
        ("*", "Align & Distribute"): "Aligner & Distribuer",
        ("*", "Stack Objects"): "Empiler les Objets",
        ("*", "Randomize"): "Aleatoire",
        ("*", "Pivot & Origin"): "Pivot & Origine",
        ("*", "Utilities"): "Utilitaires",
        ("*", "Array Placement"): "Placement en Serie",
        ("*", "Snap to Surface"): "Accrocher a la Surface",
        ("*", "Transform Presets"): "Preselections de Transformation",
        # -- Operators --
        ("*", "Quick Move"): "Deplacement Rapide",
        ("*", "Quick Rotate"): "Rotation Rapide",
        ("*", "Quick Scale"): "Echelle Rapide",
        ("*", "Align Objects"): "Aligner les Objets",
        ("*", "Distribute Objects"): "Distribuer les Objets",
        ("*", "Randomize Transform"): "Transformation Aleatoire",
        ("*", "Set Pivot"): "Definir le Pivot",
        ("*", "Move to Ground"): "Placer au Sol",
        ("*", "Move to Center"): "Placer au Centre",
        ("*", "Reset Transforms"): "Reinitialiser les Transformations",
        ("*", "Apply Transforms"): "Appliquer les Transformations",
        ("*", "Copy Transform"): "Copier la Transformation",
        ("*", "Mirror Placement"): "Placement Miroir",
        ("*", "Circular Array"): "Serie Circulaire",
        ("*", "Grid Array"): "Serie en Grille",
        ("*", "Linear Array"): "Serie Lineaire",
        ("*", "Drop to Ground"): "Deposer au Sol",
        ("*", "Snap to Active Surface"): "Accrocher a la Surface Active",
        ("*", "Save Transform Preset"): "Enregistrer la Preselection",
        ("*", "Apply Transform Preset"): "Appliquer la Preselection",
        ("*", "Delete Preset"): "Supprimer la Preselection",
        # -- Properties --
        ("*", "Move Factor"): "Facteur de Deplacement",
        ("*", "Rotate Factor"): "Facteur de Rotation",
        ("*", "Scale Factor"): "Facteur d'Echelle",
        ("*", "Gap"): "Espacement",
        ("*", "Direction"): "Direction",
        ("*", "Axis"): "Axe",
        ("*", "Mode"): "Mode",
        ("*", "Seed"): "Graine",
        ("*", "Location"): "Position",
        ("*", "Rotation"): "Rotation",
        ("*", "Scale"): "Echelle",
        ("*", "Offset"): "Decalage",
        ("*", "Count"): "Nombre",
        ("*", "Radius"): "Rayon",
        ("*", "Rows"): "Lignes",
        ("*", "Columns"): "Colonnes",
        ("*", "Layers"): "Couches",
        ("*", "Linked Duplicates"): "Duplicatas Lies",
        ("*", "Align to Normal"): "Aligner a la Normale",
    },
    "es": {
        # -- Main Panel --
        ("*", "Item Transform Pro"): "Item Transform Pro",
        ("*", "Professional Transform Toolkit"): "Herramientas de Transformacion",
        ("*", "Quick Transform"): "Transformacion Rapida",
        ("*", "Align & Distribute"): "Alinear y Distribuir",
        ("*", "Stack Objects"): "Apilar Objetos",
        ("*", "Randomize"): "Aleatorizar",
        ("*", "Pivot & Origin"): "Pivote y Origen",
        ("*", "Utilities"): "Utilidades",
        ("*", "Array Placement"): "Colocacion en Serie",
        ("*", "Snap to Surface"): "Ajustar a Superficie",
        ("*", "Transform Presets"): "Preajustes de Transformacion",
        # -- Operators --
        ("*", "Quick Move"): "Mover Rapido",
        ("*", "Quick Rotate"): "Rotar Rapido",
        ("*", "Quick Scale"): "Escalar Rapido",
        ("*", "Align Objects"): "Alinear Objetos",
        ("*", "Distribute Objects"): "Distribuir Objetos",
        ("*", "Randomize Transform"): "Transformacion Aleatoria",
        ("*", "Set Pivot"): "Establecer Pivote",
        ("*", "Move to Ground"): "Mover al Suelo",
        ("*", "Move to Center"): "Mover al Centro",
        ("*", "Reset Transforms"): "Reiniciar Transformaciones",
        ("*", "Apply Transforms"): "Aplicar Transformaciones",
        ("*", "Copy Transform"): "Copiar Transformacion",
        ("*", "Mirror Placement"): "Colocacion Espejo",
        ("*", "Circular Array"): "Serie Circular",
        ("*", "Grid Array"): "Serie en Cuadricula",
        ("*", "Linear Array"): "Serie Lineal",
        ("*", "Drop to Ground"): "Soltar al Suelo",
        ("*", "Snap to Active Surface"): "Ajustar a Superficie Activa",
        ("*", "Save Transform Preset"): "Guardar Preajuste",
        ("*", "Apply Transform Preset"): "Aplicar Preajuste",
        ("*", "Delete Preset"): "Eliminar Preajuste",
        # -- Properties --
        ("*", "Move Factor"): "Factor de Movimiento",
        ("*", "Rotate Factor"): "Factor de Rotacion",
        ("*", "Scale Factor"): "Factor de Escala",
        ("*", "Gap"): "Espacio",
        ("*", "Direction"): "Direccion",
        ("*", "Axis"): "Eje",
        ("*", "Mode"): "Modo",
        ("*", "Seed"): "Semilla",
        ("*", "Location"): "Posicion",
        ("*", "Rotation"): "Rotacion",
        ("*", "Scale"): "Escala",
        ("*", "Offset"): "Desplazamiento",
        ("*", "Count"): "Cantidad",
        ("*", "Radius"): "Radio",
        ("*", "Rows"): "Filas",
        ("*", "Columns"): "Columnas",
        ("*", "Layers"): "Capas",
        ("*", "Linked Duplicates"): "Duplicados Enlazados",
        ("*", "Align to Normal"): "Alinear a la Normal",
    },
    "zh_CN": {
        # -- Main Panel --
        ("*", "Item Transform Pro"): "Item Transform Pro",
        ("*", "Professional Transform Toolkit"): "专业变换工具箱",
        ("*", "Quick Transform"): "快速变换",
        ("*", "Align & Distribute"): "对齐与分布",
        ("*", "Stack Objects"): "堆叠对象",
        ("*", "Randomize"): "随机化",
        ("*", "Pivot & Origin"): "轴心与原点",
        ("*", "Utilities"): "实用工具",
        ("*", "Array Placement"): "阵列放置",
        ("*", "Snap to Surface"): "吸附到表面",
        ("*", "Transform Presets"): "变换预设",
        # -- Operators --
        ("*", "Quick Move"): "快速移动",
        ("*", "Quick Rotate"): "快速旋转",
        ("*", "Quick Scale"): "快速缩放",
        ("*", "Align Objects"): "对齐对象",
        ("*", "Distribute Objects"): "分布对象",
        ("*", "Randomize Transform"): "随机变换",
        ("*", "Set Pivot"): "设置轴心",
        ("*", "Move to Ground"): "移动到地面",
        ("*", "Move to Center"): "移动到中心",
        ("*", "Reset Transforms"): "重置变换",
        ("*", "Apply Transforms"): "应用变换",
        ("*", "Copy Transform"): "复制变换",
        ("*", "Mirror Placement"): "镜像放置",
        ("*", "Circular Array"): "环形阵列",
        ("*", "Grid Array"): "网格阵列",
        ("*", "Linear Array"): "线性阵列",
        ("*", "Drop to Ground"): "落到地面",
        ("*", "Snap to Active Surface"): "吸附到活动表面",
        ("*", "Save Transform Preset"): "保存变换预设",
        ("*", "Apply Transform Preset"): "应用变换预设",
        ("*", "Delete Preset"): "删除预设",
        # -- Properties --
        ("*", "Move Factor"): "移动步进",
        ("*", "Rotate Factor"): "旋转步进",
        ("*", "Scale Factor"): "缩放步进",
        ("*", "Gap"): "间距",
        ("*", "Direction"): "方向",
        ("*", "Axis"): "轴",
        ("*", "Mode"): "模式",
        ("*", "Seed"): "随机种子",
        ("*", "Location"): "位置",
        ("*", "Rotation"): "旋转",
        ("*", "Scale"): "缩放",
        ("*", "Offset"): "偏移",
        ("*", "Count"): "数量",
        ("*", "Radius"): "半径",
        ("*", "Rows"): "行",
        ("*", "Columns"): "列",
        ("*", "Layers"): "层",
        ("*", "Linked Duplicates"): "关联复制",
        ("*", "Align to Normal"): "对齐到法线",
    },
}


# ============================================================
# Translation Wrapper Function
# ============================================================

def iface_(text, context="*"):
    """
    Translate a UI string using Blender's translation system.

    Args:
        text: The English source string (message ID).
        context: Translation context (default "*" for general).

    Returns:
        Translated string if available, otherwise original text.
    """
    return bpy.app.translations.pgettext_iface(text, context)


def tip_(text, context="*"):
    """
    Translate a tooltip string.

    Args:
        text: The English source string.
        context: Translation context.

    Returns:
        Translated string if available, otherwise original text.
    """
    return bpy.app.translations.pgettext_tip(text, context)


# ============================================================
# Registration
# ============================================================

def _build_translation_dict():
    """
    Build the translation dict in the format Blender expects:
    {locale: {(context, msg_id): translated_msg}}
    """
    return TRANSLATIONS


def register():
    bpy.app.translations.register(__package__, _build_translation_dict())


def unregister():
    bpy.app.translations.unregister(__package__)
