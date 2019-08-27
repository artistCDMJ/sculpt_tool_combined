############### merge all files here for testing

bl_info = {
    "name": "Sculpt Tools UI",
    "author": "Ian Lloyd Dela Cruz, Nicholas Bishop, Roberto Roch, Bartosz Styperek, Piotr Adamowicz, Kent Trammell",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "3d View > Tool shelf, Shift-Ctrl-B",
    "description": "Simple UI for Boolean and Remesh operators",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Sculpting"}

"""if "bpy" in locals():
    import imp
    imp.reload(helper)
    imp.reload(booleanOps)
    imp.reload(greaseTrim)
    imp.reload(meshExtract)
    imp.reload(utilOps)
    imp.reload(Freeze)
    print("Reloaded multifiles")
else:
    from . import helper, booleanOps, greaseTrim, meshExtract, utilOps, Freeze
    print("Imported multifiles")"""
    
import bpy
import mathutils
import bmesh
from bpy.props import *

#################

#####################


class UI_PT_RemeshBooleanPanel(bpy.types.Panel):
    #UI panel for the Remesh and Boolean buttons
    bl_label = "Sculpt Tools"
    bl_idname = "ui_remesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sculpt"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        edit = context.preferences.edit
        wm = context.window_manager
        
        row_rem = layout.row(align=True)
        row_rem.alignment = 'EXPAND'
        row_rem.operator("sculpt.remesh", text='Remesh')
        
        row_remint = layout.row(align=True)
        row_remint.alignment = 'EXPAND'

        try:
            row_remint.prop(wm, 'remeshDepthInt', text="Depth")
            row_remint.prop(wm, 'remeshSubdivisions', text="Subdivisions")
            
        except:
            pass
            
        row_rem2 = layout.row(align=True)
        row_rem2.alignment = 'EXPAND'
        row_rem2.prop(wm, 'remeshPreserveShape', text="Preserve Shape")
        row_rem2 = layout.row(align=True)
        row_rem2.prop(wm, 'useAutoDecimate', text="Decimate")
        if wm.useAutoDecimate == True:
            row_rem2.prop(wm, "autoDecimateRatio", text="Ratio")
            
        layout.separator()
        row_freeze = layout.row(align=True)
        row_freeze.alignment = 'EXPAND'        
        row_freeze.operator("boolean.freeze", text="Freeze")
        row_freeze.operator("boolean.unfreeze", text="Unfreeze")
        layout.separator()

        row_b1 = layout.row(align=True)
        row_b1.alignment = 'EXPAND'
        row_b1.operator("boolean.union", text="Union")
        row_b1.operator("boolean.difference", text="Difference")
        row_b1.operator("boolean.intersect", text="Intersect")
        
        row_b2 = layout.row(align=True)
        row_b2.alignment = 'EXPAND'
        
        row_b2.operator("boolean.separate", text="Separate")
        row_b2.operator("boolean.clone", text="Clone")
        
        layout.separator()
        
        row_ma = layout.row(align=True)
        row_ma.alignment = 'EXPAND'
        row_ma.operator("boolean.mod_apply", text="Apply Mods")
        
        row_md = layout.row(align=True)
        row_md.alignment = 'EXPAND'
        row_md.operator("boolean.mesh_deform", text="Mesh Deform")
        
        row_dso = layout.row(align=True)
        row_dso.alignment = 'EXPAND'
        row_dso.operator("boolean.double_sided_off", text="Double Sided Off")
        
        row_sym = layout.row(align=True)
        row_sym.operator("boolean.grease_symm", text='Symmetrize')
        row_sym.prop(wm, "bolsymm", text="")
        
        row_mir = layout.row(align=True)
        row_mir.alignment = 'EXPAND'
        row_mir.operator("boolean.mod_xmirror", text="X-mirror")
        
        row_me_oprow = layout.row(align=True)
        row_me_oprow.alignment = 'EXPAND'
        row_me_oprow.operator("boolean.mask_extract", text="Extract Mask")
        
        layout.separator()
        
        row_gt = layout.row(align=True)
        row_gt.operator("boolean.grease_trim", text='Grease Cut')
        
        box = layout.box().column(align=True)
        if wm.expand_grease_settings == False: 
            box.prop(wm, "expand_grease_settings", icon="TRIA_RIGHT", icon_only=True, text=" Grease Pencil Settings", emboss=False)
        else:
            box.prop(wm, "expand_grease_settings", icon="TRIA_DOWN", icon_only=True, text=" Grease Pencil Settings", emboss=False)
            box.separator()
            box.prop(edit, "grease_pencil_manhattan_distance", text="Manhattan Distance")
            box.prop(edit, "grease_pencil_euclidean_distance", text="Euclidean Distance")
            boxrow = box.row(align=True)
            boxrow.prop(edit, "use_grease_pencil_simplify_stroke", text="Simplify")
            boxrow = box.row(align=True)
            boxrow.prop(wm, "useSubtractMode", text="Subtract")
            box.separator()                                         
            box.operator("boolean.purge_pencils", text='Purge All Grease Pencils')



class UI_MT_BooleanOpsMenu(bpy.types.Menu):
    bl_label = "Booleans"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator("boolean.union",
                        text="Union",
                        icon='ROTATECOLLECTION')
        layout.operator("boolean.difference",
                        text="Difference",
                        icon='ROTACTIVE')
        layout.operator("boolean.intersect",
                        text="Intersection",
                        icon='ROTATECENTER')


        layout.separator()
        layout.operator("boolean.separate",
                        text="Separate",
                        icon='ARROW_LEFTRIGHT')
        layout.operator("boolean.clone",
                        text="Clone",
                        icon='MOD_BOOLEAN')
        layout.separator()
        layout.operator("boolean.mod_apply",
                        text="Apply Modifiers",
                        icon='MODIFIER')
        layout.operator("boolean.grease_symm",
                        text="Symmetrize",
                        icon='MOD_MIRROR')
        layout.operator("boolean.mesh_deform",
                        text="Mesh Deform",
                        icon='MOD_MESHDEFORM')
        layout.operator("boolean.grease_trim",
                        text="Grease Cut",
                        icon='SCULPTMODE_HLT')
        layout.operator("boolean.mask_extract",
                        text="Mask Extract",
                        icon='RETOPO')




##################first
class SCULPT_OT_BooleanUnionOperator(bpy.types.Operator):
    '''Creates an union of the selected objects'''
    bl_idname = "boolean.union"
    bl_label = "Boolean Union"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)>1

    def execute(self, context):
        # add a union boolean modifier
        activeObj = context.active_object
        for SelectedObject in bpy.context.selected_objects :
            if SelectedObject != activeObj :

                helper.objSelectFaces(activeObj, 'DESELECT')
                helper.objSelectFaces(SelectedObject, 'SELECT')

                bpy.context.scene.objects.active = activeObj

                md = activeObj.modifiers.new('booleanunion', 'BOOLEAN')
                md.operation = 'UNION'
                md.object = SelectedObject       
                # apply the modifier
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleanunion")
                bpy.data.scenes.get(context.scene.name).objects.unlink(SelectedObject)
                bpy.data.objects.remove(SelectedObject)
        
        return {'FINISHED'}

class SCULPT_OT_BooleanDifferenceOperator(bpy.types.Operator):
    '''Subtracts the selection from the active object'''
    bl_idname = "boolean.difference"
    bl_label = "Boolean Difference"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)>1

    def execute(self, context):
        # add a difference boolean modifier
        activeObj = context.active_object
        for SelectedObject in bpy.context.selected_objects :
            if SelectedObject != activeObj :

                #deselect all the faces of the active object
                helper.objSelectFaces(activeObj, 'DESELECT')

                #select all the faces of the selected object
                helper.objSelectFaces(SelectedObject, 'SELECT')
                
                bpy.context.scene.objects.active = activeObj
                
                md = activeObj.modifiers.new('booleandifference', 'BOOLEAN')
                md.operation = 'DIFFERENCE'
                md.object = SelectedObject       
                # apply the modifier
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleandifference")
                bpy.data.scenes.get(context.scene.name).objects.unlink(SelectedObject)
                bpy.data.objects.remove(SelectedObject)
        
        return {'FINISHED'}

class SCULPT_OT_BooleanIntersectOperator(bpy.types.Operator):
    '''Creates an intersection of all the selected objects'''
    bl_idname = "boolean.intersect"
    bl_label = "Boolean intersect"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)>1

    def execute(self, context):
        # add a intersect boolean modifier
        activeObj = context.active_object
        for SelectedObject in bpy.context.selected_objects :
            if SelectedObject != activeObj :
                
                #deselect all the faces of the active object
                helper.objSelectFaces(activeObj, 'DESELECT')

                #select all the faces of the selected object
                helper.objSelectFaces(SelectedObject, 'SELECT')
                
                bpy.context.scene.objects.active = activeObj

                md = activeObj.modifiers.new('booleanintersect', 'BOOLEAN')
                md.operation = 'INTERSECT'
                md.object = SelectedObject       
                
                # apply the modifier
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleanintersect")
                bpy.data.scenes.get(context.scene.name).objects.unlink(SelectedObject)
                bpy.data.objects.remove(SelectedObject)
        
        return {'FINISHED'}

class SCULPT_OT_BooleanCloneOperator(bpy.types.Operator):
    '''Clones the intersecting part of the mesh'''
    bl_idname = "boolean.clone"
    bl_label = "Boolean clone"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)==2

    def execute(self, context):
        # add a intersect boolean modifier
        activeObj = context.active_object
        for SelectedObject in bpy.context.selected_objects :
            if SelectedObject != activeObj :
                
                #deselect all the faces of the active object
                helper.objSelectFaces(activeObj, 'DESELECT')

                #select all the faces of the selected object
                helper.objSelectFaces(SelectedObject, 'SELECT')

                md = SelectedObject.modifiers.new('booleanclone', 'BOOLEAN')
                md.operation = 'INTERSECT'
                md.object = activeObj       
                
                # apply the modifier
                bpy.context.scene.objects.active = SelectedObject
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="booleanclone")
                
                #restore the active object
                bpy.context.scene.objects.active = activeObj
        
        return {'FINISHED'}

class SCULPT_OT_BooleanSeparateOperator(bpy.types.Operator):
    '''Separates the active object along the intersection of the selected objects'''
    bl_idname = "boolean.separate"
    bl_label = "Boolean separation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)==2

    def execute(self, context):
        # add a intersect boolean modifier
        activeObj = context.active_object
        Selection = bpy.context.selected_objects
        
        for SelectedObject in Selection :
            if SelectedObject != activeObj :
                
                #make a copy of the selected object
                SelectedObjCopy = helper.objDuplicate(SelectedObject)
                
                #make a copy of the active object
                activeObjCopy = helper.objDuplicate(activeObj)

                helper.objSelectFaces(activeObjCopy, 'SELECT')
                helper.objSelectFaces(SelectedObject, 'DESELECT')
                
                
                md = SelectedObject.modifiers.new('sepIntersect', 'BOOLEAN')
                md.operation = 'INTERSECT'
                md.object = activeObjCopy
                # apply the modifier 
                bpy.context.scene.objects.active = SelectedObject
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="sepIntersect")
                
                helper.objSelectFaces(SelectedObject, 'INVERT')
                
                #delete the copy of the active object
                bpy.data.scenes.get(context.scene.name).objects.unlink(activeObjCopy)
                bpy.data.objects.remove(activeObjCopy)
        
        helper.objSelectFaces(SelectedObjCopy, 'SELECT')
        helper.objSelectFaces(activeObj, 'DESELECT')
   
        md2 = activeObj.modifiers.new('sepDifference', 'BOOLEAN')
        md2.operation = 'DIFFERENCE'
        md2.object = SelectedObjCopy
        
        #apply the second modifier
        bpy.context.scene.objects.active = SelectedObject
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="sepDifference")
        
        #delete the copy of the selected object
        bpy.data.scenes.get(context.scene.name).objects.unlink(SelectedObjCopy)
        bpy.data.objects.remove(SelectedObjCopy)
        
        bpy.context.active_object.select = True
        
        return {'FINISHED'}


#############################second
class SCULPT_OT_BooleanFreezeOperator(bpy.types.Operator):
    '''Decimates the object temporarily for viewport performance'''
    bl_idname = "boolean.freeze"
    bl_label = "Boolean Freeze"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)==1 and context.active_object.frozen == False

    def execute(self, context):
        
        if "Frozen" not in bpy.data.groups:
            bpy.data.groups.new("Frozen")
        
        ob = context.active_object
        obCopy = helper.objDuplicate(ob)
        md = ob.modifiers.new('BoolDecimate', 'DECIMATE')
        md.ratio = 0.1
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="BoolDecimate")
        ob.hide_render = True
        obCopy.select = True
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        obCopy.name = "Frozen_"+ob.name
        obCopy.hide = True
        obCopy.hide_select = True
        obCopy.select = False
        ob.select = True
        bpy.ops.object.group_link(group='Frozen')
        ob.frozen = True
        
        return {'FINISHED'}
        
class SCULPT_OT_BooleanUnfreezeOperator(bpy.types.Operator):
    '''Decimates the object temporarily for viewport performance'''
    bl_idname = "boolean.unfreeze"
    bl_label = "Boolean Unfreeze"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)==1 and context.active_object.frozen == True

    def execute(self, context):
        ob = bpy.context.active_object
        
        for sceneObj in bpy.context.scene.objects:
            if sceneObj.parent == ob:
                frozen = sceneObj
        
        remname = ob.data.name
        
        ob.data = bpy.context.scene.objects['Frozen_'+ob.name].data
        
        bpy.data.scenes[bpy.context.scene.name].objects.unlink(frozen)
        bpy.data.objects.remove(frozen)
        # remove mesh to prevent memory being cluttered up with hundreds of high-poly objects
        bpy.data.meshes.remove(bpy.data.meshes[remname])
        
        ob.hide_render = False
        
        bpy.data.groups['Frozen'].objects.unlink(bpy.context.object)
        
        ob.frozen = False
        
        return {'FINISHED'}


##############################third

class SCULPT_OT_GreaseTrim(bpy.types.Operator):
    """Cuts the selected object along the grease pencil stroke"""
    bl_idname = "boolean.grease_trim"
    bl_label = "Grease Cut"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod 
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'OBJECT' and context.active_object.type == 'MESH'  and 0<len(bpy.context.selected_objects)<=2

    def execute(self, context):
        objBBDiagonal = helper.objDiagonal(context.active_object)*2
        # objBBDiagonal = objBBDiagonal*2
        subdivisions = 32

        wm = bpy.context.window_manager
        noDel = []
        for ob in bpy.data.objects:
            if ob.hide == False:
                noDel.append(ob)

        if len(bpy.context.selected_objects)==1:
            try:
                mesh = bpy.context.active_object
                bpy.ops.gpencil.convert(type='POLY', timing_mode='LINEAR', use_timing_data=False)
                bpy.ops.boolean.purge_pencils()
                mesh = bpy.context.active_object
                if mesh == bpy.context.selected_objects[0]:
                    ruler = bpy.context.selected_objects[1]
                else: 
                    ruler = bpy.context.selected_objects[0]
                bpy.context.scene.objects.active = ruler
                bpy.ops.object.convert(target='MESH')
                
                rulerDiagonal = helper.objDiagonal(ruler)
                verts = []
                
                bm = bmesh.new()
                bm.from_mesh(ruler.data)
                
                for v in bm.verts:
                    if len(v.link_edges) == 1:
                        v.select = True
                        verts.append(v)
                dist = verts[0].co - verts[1].co
                if dist.length < rulerDiagonal/10:
                    bm.edges.new(verts)
                
                bm.to_mesh(ruler.data)
                
            except:
                self.report({'WARNING'}, "Draw a line with grease pencil first")
                return {'FINISHED'}
        elif len(bpy.context.selected_objects)==2:
            mesh = bpy.context.active_object
            
            if mesh == bpy.context.selected_objects[0]:
                ruler = bpy.context.selected_objects[1]
            else: 
                ruler = bpy.context.selected_objects[0]
            
            if ruler.type == 'MESH' and len(ruler.data.polygons)>0:
                bpy.context.scene.objects.active = ruler
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type="EDGE")
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.region_to_loop()
                bpy.ops.mesh.select_all(action='INVERT')
                bpy.ops.mesh.delete(type='EDGE')
                bpy.ops.object.mode_set(mode='OBJECT')
            elif ruler.type == 'CURVE':
                bpy.context.scene.objects.active = ruler
                bpy.ops.object.convert(target='MESH')
            


        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                viewZAxis = tuple([z * objBBDiagonal for z in area.spaces[0].region_3d.view_matrix[2][0:3]])
                negViewZAxis = tuple([z * (-2*objBBDiagonal*(1/subdivisions)) for z in area.spaces[0].region_3d.view_matrix[2][0:3]])
                break
        
        bpy.context.scene.objects.active = ruler

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.select_mode(type="EDGE")
        bpy.ops.transform.translate(value = viewZAxis)
        for i in range(0, subdivisions):
            bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":negViewZAxis})
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = mesh
        bpy.ops.boolean.separate()

        if wm.useSubtractMode:
            for ob in bpy.data.objects:
                if ob not in noDel:
                    bpy.data.scenes[0].objects.unlink(ob)
                    bpy.data.objects.remove(ob)
    
        return {'FINISHED'}

class SCULPT_OT_PurgeAllPencils(bpy.types.Operator):
    """Removes all Grease Pencil Layers"""
    bl_idname = "boolean.purge_pencils"
    bl_label = "Clears all grease pencil user data in the scene"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        if not context.scene.grease_pencil == None:
            context.scene.grease_pencil.clear()
        for obj in context.scene.objects:
            if not context.scene.objects[obj.name].grease_pencil == None:
                context.scene.objects[obj.name].grease_pencil.clear() 
        return {'FINISHED'}


###############################fourth
def objSelectFaces(obj, mode):
    
    #store active object
    activeObj = bpy.context.active_object
    
    #store the mode of the active object
    oldMode = activeObj.mode
    
    #perform selection
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action=mode)
    
    #restore old active object and mode
    bpy.ops.object.mode_set(mode=oldMode)
    bpy.context.scene.objects.active = activeObj

#helper function to duplicate an object    
def objDuplicate(obj):

    activeObj = bpy.context.active_object
    oldMode = activeObj.mode    

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action = 'DESELECT')
    bpy.ops.object.select_pattern(pattern = obj.name)
    bpy.ops.object.duplicate()
    objCopy = bpy.context.selected_objects[0]

    bpy.context.scene.objects.active = activeObj
    bpy.ops.object.mode_set(mode=oldMode)
    return objCopy
    
def objDiagonal(obj):
    return ((obj.dimensions[0]**2)+(obj.dimensions[1]**2)+(obj.dimensions[2]**2))**0.5
    
def objDelete(obj):
    rem = obj
    remname = rem.data.name
    bpy.data.scenes[bpy.context.scene.name].objects.unlink(rem)
    bpy.data.objects.remove(rem)
    # remove mesh to prevent memory being cluttered up with hundreds of high-poly objects
    bpy.data.meshes.remove(bpy.data.meshes[remname])


###################################fifth
class SCULPT_OT_MaskExtractOperator(bpy.types.Operator):
    """Extracts the masked area into a new mesh"""
    bl_idname = "boolean.mask_extract"
    bl_label = "Mask Extract"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'
    
    def draw(self, context): 
        wm = context.window_manager
        layout = self.layout
        layout.prop(wm, "extractStyleEnum", text="Style")
        layout.prop(wm, "extractDepthFloat", text="Depth")
        layout.prop(wm, "extractOffsetFloat", text="Offset")
        layout.prop(wm, "extractSmoothIterationsInt", text="Smooth Iterations")
    
    def execute(self, context):
        wm = context.window_manager
        activeObj = context.active_object
        
        # This is a hackish way to support redo functionality despite sculpt mode having its own undo system.
        # The set of conditions here is not something the user can create manually from the UI.
        # Unfortunately I haven't found a way to make Undo itself work
        if  2>len(bpy.context.selected_objects)>0 and \
            context.selected_objects[0] != activeObj and \
            context.selected_objects[0].name.startswith("Extracted."):
            rem = context.selected_objects[0]
            remname = rem.data.name
            bpy.data.scenes.get(context.scene.name).objects.unlink(rem)
            bpy.data.objects.remove(rem)
            # remove mesh to prevent memory being cluttered up with hundreds of high-poly objects
            bpy.data.meshes.remove(bpy.data.meshes[remname])
        
        # For multires we need to copy the object and apply the modifiers
        try:
            if activeObj.modifiers["Multires"]:
                use_multires = True
                objCopy = helper.objDuplicate(activeObj)
                bpy.context.scene.objects.active = objCopy
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.boolean.mod_apply()
        except:
            use_multires = False
            pass
            
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Automerge will collapse the mesh so we need it off.
        if context.scene.tool_settings.use_mesh_automerge:
            automerge = True
            bpy.data.scenes[context.scene.name].tool_settings.use_mesh_automerge = False
        else:
            automerge = False

        # Until python can read sculpt mask data properly we need to rely on the hiding trick
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent();
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate=None, TRANSFORM_OT_translate=None)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='EDIT')
        
        # For multires we already have a copy, so lets use that instead of separate.
        if use_multires == True:
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.delete(type='FACE')
            bpy.context.scene.objects.active = objCopy;
        else:
            try:
                bpy.ops.mesh.separate(type="SELECTED")
                bpy.context.scene.objects.active = context.selected_objects[0];
            except:
                bpy.ops.object.mode_set(mode='SCULPT')
                bpy.ops.paint.hide_show(action='SHOW', area='ALL')
                return {'FINISHED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rename the object for disambiguation
        bpy.context.scene.objects.active.name = "Extracted." + bpy.context.scene.objects.active.name
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Solid mode should create a two-sided mesh
        if wm.extractStyleEnum == 'SOLID':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.shrink_fatten(value=-wm.extractOffsetFloat) #offset
            bpy.ops.mesh.region_to_loop()
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.vertices_smooth(repeat = wm.extractSmoothIterationsInt) #smooth everything but border edges to sanitize normals
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.solidify(thickness = -wm.extractDepthFloat)
            bpy.ops.mesh.select_all(action='SELECT')
            if wm.extractSmoothIterationsInt>0: bpy.ops.mesh.vertices_smooth(repeat = wm.extractSmoothIterationsInt)
            bpy.ops.mesh.normals_make_consistent();

        elif wm.extractStyleEnum == 'SINGLE':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.shrink_fatten(value=-wm.extractOffsetFloat) #offset
            bpy.ops.mesh.region_to_loop()
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.vertices_smooth(repeat = wm.extractSmoothIterationsInt) #smooth everything but border edges to sanitize normals
            bpy.ops.mesh.select_all(action='SELECT')
            # This is to create an extra loop and prevent the bottom vertices running up too far in smoothing
            # Tried multiple ways to prevent this and this one seemed best
            bpy.ops.mesh.inset(thickness=0, depth=wm.extractDepthFloat/1000, use_select_inset=False)
            bpy.ops.mesh.inset(thickness=0, depth=wm.extractDepthFloat-(wm.extractDepthFloat/1000), use_select_inset=False)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.vertices_smooth(repeat = wm.extractSmoothIterationsInt)
            bpy.ops.mesh.normals_make_consistent()

        elif wm.extractStyleEnum == 'FLAT':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            # Offset doesn't make much sense for Flat mode, so let's add it to the depth to make it a single op.
            bpy.ops.transform.shrink_fatten(value=-wm.extractDepthFloat-wm.extractOffsetFloat) 
            if wm.extractSmoothIterationsInt>0: bpy.ops.mesh.vertices_smooth(repeat = wm.extractSmoothIterationsInt)
            
        # clear mask on the extracted mesh
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # make sure to recreate the odd selection situation for redo
        if use_multires:
            bpy.ops.object.select_pattern(pattern=context.active_object.name, case_sensitive=True, extend=False)
        bpy.context.scene.objects.active = activeObj
        
        # restore automerge
        if automerge:
            bpy.data.scenes[context.scene.name].tool_settings.use_mesh_automerge = True

        # restore mode for original object
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}


###############################sixth
class SCULPT_OT_BooleanMeshDeformOperator(bpy.types.Operator):
    '''Binds a deforming mesh to the object'''
    bl_idname = "boolean.mesh_deform"
    bl_label = "Mesh deform"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(bpy.context.selected_objects)==2

    def execute(self, context):
        activeObj = context.active_object
        for SelectedObject in bpy.context.selected_objects :
            if SelectedObject != activeObj :
                md = activeObj.modifiers.new('mesh_deform', 'MESH_DEFORM')
                md.object = SelectedObject
                bpy.ops.object.meshdeform_bind(modifier="mesh_deform")
                bpy.context.scene.objects.active = SelectedObject
                SelectedObject.draw_type="WIRE"
                bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}
    
class SCULPT_OT_ModApplyOperator(bpy.types.Operator):
    '''Applies all modifiers for all selected objects. Also works in sculpt or edit mode.'''
    bl_idname = "boolean.mod_apply"
    bl_label = "Apply Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        activeObj = context.active_object
        for SelectedObject in bpy.context.selected_objects :
               
            bpy.context.view_layer.objects.active = SelectedObject
            oldMode = SelectedObject.mode    
            bpy.ops.object.mode_set(mode='OBJECT')
            for md in SelectedObject.modifiers :
                # apply the modifier
                try:
                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=md.name)
                except:
                    pass
            bpy.ops.object.mode_set(mode=oldMode)
        bpy.context.view_layer.objects.active = activeObj
        return {'FINISHED'}
    
class SCULPT_OT_RemeshOperator(bpy.types.Operator):
    '''Remesh an object at the given octree depth'''
    bl_idname = "sculpt.remesh"
    bl_label = "Sculpt Remesh"

    bl_options = {'REGISTER', 'UNDO'}
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def draw(self, context): 
        if context.active_object.mode != 'SCULPT':   
            wm = context.window_manager
            layout = self.layout
            layout.prop(wm, "remeshDepthInt", text="Depth")
            layout.prop(wm, "remeshSubdivisions", text="Subdivisions")
            layout.prop(wm, "remeshPreserveShape", text="Preserve Shape")
        
    def execute(self, context):
        # add a smooth remesh modifier
        ob = context.active_object
        wm = context.window_manager
        oldMode = ob.mode
        
        dyntopoOn = False;
        if context.active_object.mode == 'SCULPT': 
            if context.sculpt_object.use_dynamic_topology_sculpting:
                dyntopoOn = True
                bpy.ops.sculpt.dynamic_topology_toggle()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        if wm.remeshPreserveShape:            
            obCopy = helper.objDuplicate(ob)
        
        md = ob.modifiers.new('sculptremesh', 'REMESH')
        md.mode = 'SMOOTH'
        md.octree_depth = wm.remeshDepthInt
        md.scale = .99
        md.use_remove_disconnected = False

        # apply the modifier
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="sculptremesh")
        
        if wm.remeshSubdivisions > 0:
            mdsub = ob.modifiers.new('RemeshSubSurf', 'SUBSURF')
            mdsub.levels = wm.remeshSubdivisions
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="RemeshSubSurf")
        
        
        if wm.remeshPreserveShape:            
            md2 = ob.modifiers.new('RemeshShrinkwrap', 'SHRINKWRAP')
            md2.wrap_method = 'PROJECT'
            md2.use_negative_direction = True
            md2.use_positive_direction = True
            md2.target = obCopy
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="RemeshShrinkwrap")
            
            bpy.data.scenes.get(context.scene.name).objects.unlink(obCopy)
            bpy.data.objects.remove(obCopy)
        
        if wm.useAutoDecimate == True:
            dec = ob.modifiers.new("decimator", "DECIMATE")
            dec.ratio = wm.autoDecimateRatio
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier="decimator")

        bpy.ops.object.mode_set(mode=oldMode)
        
        if dyntopoOn == True:
            bpy.ops.sculpt.dynamic_topology_toggle()
        
        ob.select = True
        return {'FINISHED'}
        

        
class SCULPT_OT_XMirrorOperator(bpy.types.Operator):
    '''Applies an X-axis mirror modifier to the selected object. If more objects are selected, they will be mirrored around the active object.'''
    bl_idname = "boolean.mod_xmirror"
    bl_label = "X-Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
    
    def execute(self, context):
        activeObj = context.active_object
        if len(bpy.context.selected_objects)>1 :
            for SelectedObject in bpy.context.selected_objects :
                if SelectedObject != activeObj :
                    oldMode = SelectedObject.mode    

                    bpy.context.scene.objects.active = SelectedObject

                    bpy.ops.object.mode_set(mode='OBJECT')

                    md = SelectedObject.modifiers.new('xmirror', 'MIRROR')
                    md.mirror_object = activeObj



                    bpy.ops.object.mode_set(mode=oldMode)
                    bpy.context.scene.objects.active = activeObj
                    
        #if there's only one object selected, apply straight fo the active obj.
        if len(bpy.context.selected_objects)==1 :

            oldMode = activeObj.mode    

            bpy.ops.object.mode_set(mode='OBJECT')

            md = activeObj.modifiers.new('xmirror', 'MIRROR')

            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=md.name)

            bpy.ops.object.mode_set(mode=oldMode)
                
        return {'FINISHED'}

        
class SCULPT_OT_DoubleSidedOffOperator(bpy.types.Operator):
    '''Turn off double sided for all objects'''
    bl_idname = "boolean.double_sided_off"
    bl_label = "Double Sided Off"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        for mesh in bpy.data.meshes:
            mesh.show_double_sided = False
        return {'FINISHED'}

class SymmetrizeBoolMesh(bpy.types.Operator):
    """Copies one side of the mesh to the other along the chosen axis"""
    bl_idname = "boolean.grease_symm"
    bl_label = "Bool Mesh Symm Function"
    bl_options = {'REGISTER', 'UNDO'}
    
    symm_int = bpy.props.FloatProperty(name="Threshold", min = 0.0001, max = 1, default = .001)       
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'OBJECT' and context.active_object.type == 'MESH' or context.active_object is not None and context.active_object.mode == 'VERTEX_PAINT'

    def execute(self, context):
        func = bpy.ops
        wm = context.window_manager
        mode_curr = context.active_object.mode
        func.object.editmode_toggle()
        func.mesh.select_all(action='SELECT')
        func.mesh.symmetrize(direction = wm.bolsymm, threshold= self.symm_int)
        func.mesh.remove_doubles()
        func.object.editmode_toggle()
        if mode_curr == 'VERTEX_PAINT':
            func.object.mode_set(mode='VERTEX_PAINT')
        return {'FINISHED'}
    
    


classes = (
            UI_PT_RemeshBooleanPanel,
            SCULPT_OT_BooleanUnionOperator,
            SCULPT_OT_BooleanDifferenceOperator,
            SCULPT_OT_BooleanIntersectOperator,
            SCULPT_OT_BooleanCloneOperator,
            SCULPT_OT_BooleanSeparateOperator,
            SCULPT_OT_BooleanUnfreezeOperator,
            SCULPT_OT_BooleanFreezeOperator,
            SCULPT_OT_GreaseTrim,
            SCULPT_OT_PurgeAllPencils,
            SCULPT_OT_MaskExtractOperator,
            SCULPT_OT_BooleanMeshDeformOperator,
            SCULPT_OT_ModApplyOperator,
            SCULPT_OT_RemeshOperator,
            SCULPT_OT_XMirrorOperator,
            
            
            
)
        

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new('wm.call_menu', 'B', 'PRESS', ctrl = True, shift = True)
        kmi.properties.name = "BooleanOpsMenu"
        
        kmi = km.keymap_items.new('sculpt.optimize', 'U', 'PRESS')
        
        kmi = km.keymap_items.new('wm.context_toggle', 'X', 'PRESS')
        kmi.properties.data_path = "tool_settings.sculpt.use_symmetry_x"
        
        kmi = km.keymap_items.new('wm.context_toggle', 'E', 'PRESS', shift = True)
        kmi.properties.data_path = "tool_settings.sculpt.use_edge_collapse"
        
        kmi = km.keymap_items.new('sculpt.dynamic_topology_toggle', 'D', 'PRESS', shift = True)

    bpy.types.Object.frozen = BoolProperty(name="frozen", default = False)
        
    bpy.types.WindowManager.remeshDepthInt = IntProperty(min = 2, max = 10, default = 4)
    bpy.types.WindowManager.remeshSubdivisions = IntProperty(min = 0, max = 6, default = 0)
    bpy.types.WindowManager.remeshPreserveShape = BoolProperty(default = True)
    bpy.types.WindowManager.useAutoDecimate = BoolProperty(default = False)
    bpy.types.WindowManager.autoDecimateRatio = FloatProperty(min = 0.00, max = 1.00, default = 0.10)
    bpy.types.WindowManager.useSubtractMode = BoolProperty(default = True)

    bpy.types.WindowManager.extractDepthFloat = FloatProperty(min = -10.0, max = 10.0, default = 0.1)
    bpy.types.WindowManager.extractOffsetFloat = FloatProperty(min = -10.0, max = 10.0, default = 0.0)

    bpy.types.WindowManager.extractSmoothIterationsInt = IntProperty(min = 0, max = 50, default = 5)
    
    bpy.types.WindowManager.extractStyleEnum = EnumProperty(name="Extract style",
                     items = (("SOLID","Solid",""),
                              ("SINGLE","Single Sided",""),
                              ("FLAT","Flat","")),
                     default = "SOLID")
    
    bpy.types.WindowManager.expand_grease_settings = BoolProperty(default=False)

    bpy.types.WindowManager.bolsymm = EnumProperty(name="",
                     items = (("NEGATIVE_X","-X to +X",""),
                              ("POSITIVE_X","+X to -X",""),
                              ("NEGATIVE_Y","-Y to +Y",""),
                              ("POSITIVE_Y","+Y to -Y",""),
                              ("NEGATIVE_Z","-Z to +Z",""),
                              ("POSITIVE_Z","+Z to -Z","")),                                                                                           
                     default = "NEGATIVE_X")
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps["3D View"]
        for kmi in km.keymap_items:
            if kmi.idname == 'wm.call_menu':
                if kmi.properties.name == "BooleanOpsMenu":
                    km.keymap_items.remove(kmi)
                    break
    try:
        del bpy.types.WindowManager.remeshDepthInt
        del bpy.types.WindowManager.expand_grease_settings
        del bpy.types.WindowManager.extractDepthFloat
        del bpy.types.WindowManager.extractSmoothIterationsInt
        del bpy.types.WindowManager.bolsymm
        
    except:
        pass

if __name__ == "__main__":
    register()

