import pygame as pg
import os

pg.init()
pg.mixer.init()

screen = pg.display.set_mode((1280, 720))
font = pg.font.SysFont("Impact", 38)

# Define folder paths for different instruments
wav_folders = {
    'violin': "C:/Users/Ysobel Vera/Documents/AllSingleNotes/violin-single-notes",
    'trumpet': "C:/Users/Ysobel Vera/Documents/AllSingleNotes/trumpet-single-notes",
    'flute': "C:/Users/Ysobel Vera/Documents/AllSingleNotes/flute-single-notes",
    'snare': "C:/Users/Ysobel Vera/Documents/AllSingleNotes/snare-single-notes"
}

# Initialize with violin folder
current_folder = 'violin'
wav_folder = wav_folders[current_folder]

keylist = '1234567890qwertyuiopasdfghjklzxcvbnm,.'

# Function to load notes from the currently selected folder
def load_notes():
    global wav_folder
    notes = {}
    posx, posy = 25, 25

    # Load the notes list from the text file
    with open("master-notelist.txt") as notes_file:
        noteslist = notes_file.read().splitlines()

    # Ensure the lists match or handle the mismatch
    if len(noteslist) > len(keylist):
        print("Warning: More notes than keys! Truncating notes list.")
        noteslist = noteslist[:len(keylist)]  # Truncate noteslist to match keylist

    for i in range(len(noteslist)):
        if i >= len(keylist):  # Prevent index out of range
            break

        key = keylist[i]

        # Construct the filename for the wav file
        wav_file = os.path.join(wav_folder, f"{noteslist[i]}.wav")

        if os.path.exists(wav_file):
            sample = pg.mixer.Sound(wav_file)
            print(f"Loaded: {wav_file}")  # Debugging print to ensure file is loaded
        else:
            print(f"File {wav_file} not found!")  # Debugging message for missing files
            continue

        color = [int(x) for x in (255 * (i / len(noteslist)), 200, 150)]
        notes[key] = [sample, noteslist[i], (posx, posy), color]
        notes[key][0].set_volume(0.33)

        screen.blit(font.render(notes[key][1], 0, notes[key][3]), (posx, posy))

        posx += 140
        if posx > 1220:
            posx, posy = 25, posy + 56

    pg.display.update()
    return notes

# Load initial notes
notes = load_notes()

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False
        if event.type == pg.KEYDOWN:
            key = str(event.unicode)
            if key in notes:
                notes[key][0].play()  # Play the sound associated with the key
                screen.blit(font.render(notes[key][1], 0, (255, 255, 255)), notes[key][2])
            elif key == '/':  # Press '/' to switch instruments
                # Switch instrument folder
                instrument_keys = list(wav_folders.keys())
                current_index = instrument_keys.index(current_folder)
                current_folder = instrument_keys[(current_index + 1) % len(instrument_keys)]
                wav_folder = wav_folders[current_folder]
                print(f"Switching to {current_folder} notes...")

                # Reload notes from the new folder
                pg.mixer.stop()  # Stop any currently playing sounds
                screen.fill((0, 0, 0))  # Clear the screen
                notes = load_notes()  # Reload notes

        if event.type == pg.KEYUP and str(event.unicode) != '' and str(event.unicode) in notes:
            key = str(event.unicode)
            if key in notes:
                notes[key][0].fadeout(100)
                screen.blit(font.render(notes[key][1], 0, notes[key][3]), notes[key][2])

    pg.display.update()

pg.display.set_caption("Exporting sound sequence")

pg.mixer.quit()
pg.quit()