import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper


bl_info = {
    "name": "SporeModder Add-ons",
    "author": "emd4600",
    "blender": (2, 80, 0),
    "version": (2, 1, 0),
    "location": "File > Import-Export",
    "description": "Import Spore .gmdl and .rw4 model formats. Export .rw4 format.",
    "category": "Import-Export"
}


class ImportGMDL(bpy.types.Operator, ImportHelper):
    bl_idname = "import_my_format.gmdl"
    bl_label = "Import GMDL"

    filename_ext = ".gmdl"
    filter_glob: bpy.props.StringProperty(default="*.gmdl", options={'HIDDEN'})

    def execute(self, context):
        from .gmdl_importer import import_gmdl

        file = open(self.filepath, 'br')
        result = {'CANCELLED'}
        try:
            result = import_gmdl(file, False)
        finally:
            file.close()

        return result


class ImportRW4(bpy.types.Operator, ImportHelper):
    bl_idname = "import_my_format.rw4"
    bl_label = "Import RW4"

    filename_ext = ".rw4"
    filter_glob: bpy.props.StringProperty(default="*.rw4", options={'HIDDEN'})

    import_materials: bpy.props.BoolProperty(
        name="Import Materials",
        description="",
        default=True
    )
    import_skeleton: bpy.props.BoolProperty(
        name="Import Skeleton [EXPERIMENTAL]",
        description="",
        default=True
    )
    import_movements: bpy.props.BoolProperty(
        name="Import Movements [EXPERIMENTAL]",
        description="If present, import animations and morphs",
        default=False
    )

    def execute(self, context):
        from .rw4_importer import RW4ImporterSettings, import_rw4

        settings = RW4ImporterSettings()
        settings.import_materials = self.import_materials
        settings.import_skeleton = self.import_skeleton
        settings.import_movements = self.import_movements

        file = open(self.filepath, 'br')
        result = {'CANCELLED'}
        try:
            result = import_rw4(file, settings)
        finally:
            file.close()

        return result


class ExportRW4(bpy.types.Operator, ExportHelper):
    bl_idname = "export_my_format.rw4"
    bl_label = "Export RW4"

    filename_ext = ".rw4"
    filter_glob: bpy.props.StringProperty(default="*.rw4", options={'HIDDEN'})

    def execute(self, context):
        from .rw4_exporter import export_rw4

        file = open(self.filepath, 'bw')
        result = {'CANCELLED'}
        try:
            result = export_rw4(file)
        finally:
            file.close()
        return result


def gmdl_importer_menu_func(self, context):
    self.layout.operator(ImportGMDL.bl_idname, text="Spore GMDL Model (.gmdl)")


def rw4_importer_menu_func(self, context):
    self.layout.operator(ImportRW4.bl_idname, text="Spore RenderWare 4 (.rw4)")


def rw4_exporter_menu_func(self, context):
    self.layout.operator(ExportRW4.bl_idname, text="Spore RenderWare 4 (.rw4)")


classes = (
    ImportGMDL,
    ImportRW4,
    ExportRW4
)


def register():
    from . import rw4_material_config, rw4_animation_config

    rw4_material_config.register()
    rw4_animation_config.register()

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.TOPBAR_MT_file_import.append(gmdl_importer_menu_func)
    bpy.types.TOPBAR_MT_file_import.append(rw4_importer_menu_func)
    bpy.types.TOPBAR_MT_file_export.append(rw4_exporter_menu_func)


def unregister():
    from . import rw4_material_config, rw4_animation_config

    rw4_material_config.unregister()
    rw4_animation_config.unregister()

    for c in classes:
        bpy.utils.unregister_class(c)

    bpy.types.TOPBAR_MT_file_import.remove(gmdl_importer_menu_func)
    bpy.types.TOPBAR_MT_file_import.remove(rw4_importer_menu_func)
    bpy.types.TOPBAR_MT_file_export.remove(rw4_exporter_menu_func)


if __name__ == "__main__":
    register()
