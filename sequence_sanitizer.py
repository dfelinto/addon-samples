import bpy
import os

def sanitize_filepath(sound):
    """
    Remove duplicated folder paths.
    I cleared this up in the system side, yet
    I need to update the strips.
    """

    # Split the filepath in ['//.., 'My_Folder', 'My_Other_Folder', 'filepath.wav']
    parts = sound.filepath.split(os.sep)

    # Nothing to do here, nothing duplicated
    if len(set(parts)) == len(parts):
        return

    # Quick production hack for clarity
    all_parts = []
    prev = ""
    for part in parts:
        if part == prev:
            continue
        prev = part
        all_parts.append(part)

    filepath_new = os.sep.join(all_parts)

    print(sound.filepath + " > " + filepath_new)
    sound.filepath = filepath_new


for scene in bpy.data.scenes:
    for sequence in scene.sequence_editor.sequences:
        sanitize_filepath(sequence.sound)
