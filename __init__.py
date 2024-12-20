# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Texture Upscaler",
    "author": "Hasib345",
    "version": (0,6),
    "blender": (3, 00, 0),
    "location": "Image Editor > N-Panel > Texture Upscaler ",
    "description": "Upscale Textures",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://justsomerender.gumroad.com/l/TextureUpscaler",
    "category": "Image Editor"}


import glob
import bpy
import os
import subprocess
import time


class TU_image_Panel(bpy.types.Panel):
    """Panel to Upscale Textures"""
    bl_idname = "IMAGE_EDITOR_PT_texture_upscaler"
    bl_label = "Texture Upscaler"
    #bl_options =  {'DEFAULT_CLOSED'}

    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Texture Upscaler"
    

    def draw(self, context):
        layout = self.layout
        im = context.space_data.image
        prop = context.preferences.addons[__name__].preferences
        
        try:
            layout.label(text=f'Image: {im.name}')
            # layout.use_property_split = True

            layout.label(text=f'Current Resolution: {im.size[0]}X{im.size[1]}')
            layout.label(text=f'Resolution After Upscale: {im.size[0]*int(prop.scale)}X{im.size[1]*int(prop.scale)}')

            layout.prop(prop, 'replace_image' , text='Replace Texture in Material'  ,expand=True)

            layout.prop(prop, 'scale' , expand=True)
            layout.prop(context.scene,'models')
        except:
            layout.label(text="No Active Texture")
        layout.operator(TU_image_Upscaler.bl_idname)




class TU_image_Upscaler(bpy.types.Operator):
    """Upscales the active images in image editor"""
    bl_idname = "active_image.upscale"
    bl_label = "Texture Upscaler"
    has_reports = True

    @classmethod
    def poll(cls, context):
        return context.space_data.image is not None 



    def execute(self, context):
        bpy.ops.wm.console_toggle()
        # Store the original sys.path to restore later
        start_time = time.time()
        # Get the preferences and image from the context
        prop = context.preferences.addons[__name__].preferences
        image = context.space_data.image
        # Generate the file path to save the image
        if image.file_format.lower() in image.name.lower():
            file_path = os.path.join(prop.path, image.name)
            print(file_path)
        else:
            file_path = os.path.join(prop.path, f'{image.name}.{image.file_format.lower()}')

        # Save the image to the file path
        image.save(filepath=file_path, quality=100)
        # Generate the save path for the upscaled image
        model = context.scene.models
        # Upscale the image
        scale = int(prop.scale)
        base, ext = os.path.splitext(image.name)
        new_path = os.path.join(prop.path, f'{base}_Upscaled{scale}x.{image.file_format.lower()}')
        addon_dir = os.path.dirname(os.path.realpath(__file__))
        exe_file = os.path.join(addon_dir, "realesrgan-ncnn-vulkan.exe")
        if prop.gpu == "Auto":
            command = rf'{exe_file} -i "{file_path}" -o "{new_path}"  -n  {model} -s {scale} '
        else:
            command = rf'{exe_file} -i "{file_path}" -o "{new_path}"  -n  {model} -s {scale} -g {int(prop.gpu)}'
        try:
            subprocess.call(command)
            upscaled_image = bpy.data.images.load(new_path)
            
        except Exception as ex:
            self.report({'ERROR'}, str({ex}))
            return {'CANCELLED'}
        

        bpy.ops.wm.console_toggle()
        if prop.replace_image:
                replace_image_nodes(image, upscaled_image)
            # Set the upscaled image as the active image in the context
        context.space_data.image = upscaled_image
        end_time = time.time()
        duration = end_time - start_time
        self.report({'INFO'}, f"Upscaled image in {duration} seconds")
        return {'FINISHED'}

def replace_image_nodes(old_image ,Upscaled_image):
    material  = bpy.data.materials

    for mat in material:
        try:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image == old_image:
                        node.image = Upscaled_image
        except Exception as ex:
            print(f'Error While Replacing Texture in Image Nodes: {ex}')


class TU_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    path: bpy.props.StringProperty(
        name='Path to save upscaled images',
        description='Set the path where you want to save images textures \n Make sure path has permission to write',
        default=r"C:\tmp",
        subtype='DIR_PATH'
    )
    scale:bpy.props.EnumProperty(items = [
        ('2', '2x', '2'),
        ('3', '3x', '3'),
        ('4', '4x', '4'),
        ],
    name= 'Select Scale Level:',
    description = "Scale Level for Upscaling",
    default='4'
    )
    replace_image: bpy.props.BoolProperty(
        name='Replace Image',
        description='Replace Image with Upscaled Image',
        default=False
    )
    gpu:bpy.props.EnumProperty(items = [
        ('Auto', 'Auto', 'Auto'),
        ('0', 'Device 0', '0'),
        ('1', 'Device 1', '1'),
        ('2', 'Device 2', '2'),
        ],
    name= 'Select Gpu device',
    description = "Gpu device to use For Upscaling \n Leave Auto if you are not sure \n Device 0 is mostly Cpu and Device 1 and Device 2 is mostly Gpu",
    default='Auto'
    )
    def draw(self, context):
        layout = self.layout
        layout.label(text="Add the path where the images will be saved.")
        layout.prop(self, "path")
        layout.prop(self, "gpu")
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Option to add your custom ncnn Model" , icon = 'INFO')
        col.operator("texture_upscaler.import_model" , text="Add Model", icon = 'FILE_FOLDER')


from .model import get_models, model_importer
classes = (
    TU_image_Upscaler,
    TU_image_Panel,
    model_importer,
    TU_Preferences,
    
)


def register():
    bpy.types.Scene.models = bpy.props.EnumProperty(items=get_models())
    for cls in classes:
        bpy.utils.register_class(cls)
    

def unregister():
    del bpy.types.Scene.models
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
