import bpy
from bgl import *


def view_setup():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glOrtho(0, 1, 0, 1, -15, 15)
    gluLookAt(0.0, 0.0, 1.0, 0.0,0.0,0.0, 0.0,1.0,0.0)


def view_reset(viewport):
    # Get texture info
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glViewport(viewport[0], viewport[1], viewport[2], viewport[3])


def draw_rectangle(region, width, height, size=0.25, zed=0.0):
    coordinates = [(size, size), (0, size), (0, 0), ( size, 0)]

    verco = []
    for x,y in coordinates:
        co = list(region.view2d.view_to_region(x,y, False))
        co[0] /= float(width)
        co[1] /= float(height)
        verco.append(co)

    glPolygonMode(GL_FRONT_AND_BACK , GL_FILL)
    glEnable(GL_BLEND)
    glBegin(GL_QUADS)
    for i in range(4):
        glColor4f(1.0, 1.0, 0.0, 0.5)
        glVertex2f(verco[i][0], verco[i][1])
    glEnd()
    glDisable(GL_BLEND)


def get_clipeditor_region():
    for area in bpy.context.screen.areas:
        if area.type == 'CLIP_EDITOR':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return region, region.width, region.height

    return None, 0, 0


@bpy.app.handlers.persistent
def draw_rectangle_callback_px(not_used):
    import blf

    if len(bpy.data.movieclips) < 1:
        return

    scene = bpy.context.scene
    movieclip = bpy.data.movieclips[0]

    region, width, height = get_clipeditor_region()
    if not region:
        return

    viewport = Buffer(GL_INT, 4)
    glGetIntegerv(GL_VIEWPORT, viewport)

    # set identity matrices
    view_setup()

    draw_rectangle(region, width, height, 1.0)

    # restore opengl defaults
    view_reset(viewport)
    glColor4f(1.0, 1.0, 1.0, 1.0)


    # draw some text
    font_id = 0

    # draw some text
    blf.position(font_id, 15, 30, 0)
    blf.size(font_id, 20, 72)
    blf.draw(font_id, "Movie Clip: {0}".format(movieclip.name))


def register():
    bpy._handle = bpy.types.SpaceClipEditor.draw_handler_add(draw_rectangle_callback_px, (None,), 'WINDOW', 'POST_PIXEL')


def unregister():
    bpy.types.SpaceClipEditor.draw_handler_remove(bpy._handle, 'WINDOW')


if __name__ == "__main__":
    register()

