# Python_Synth
A simple synthetizer made with Pygame and Numpy in Python.
## What is a soundwave
Soundwaves are pressure fluctuations which travel trough the air (or other physical medium) and hit your eardrums. We can generate these waves with a speaker, which usually consists of a dyaphragm wuth an electrical coil attached and a permanent magnet. When an electrical signal passed through the coil it vibrates the diaphragm and which in turn moves the air around it creating soundwaves.

The electrical signal consists of an alternating current, usually created by a DAC - Digital Analog Converter and amplified bya a amplifier. Before that, the signal is digital, consisting of ones and zeros in your computer.

And what does this digital signal look like? Basically it is a long list of numbers.

## Generating a digital signal
The first thing we should consider when generating a digital signal is the sampling rate, that is, how many values we need to define for a second of sound. The default value for the Pygame mixer is 41000 samples per second, so that's what I'll be using.

The second thing is the form of the wave, responsible for the quality of the sound, or timbre, the reason why different instruments sound so dissimilar for the same frequency or pitch. The most pure waveform is the sine, also one of the easiest to generate in numpy, but the are inumerous other types, like square, triangular and sawtooth.

We will start with the sine wave, which will actually be generated by the cosine function (makes things easier for triangular waves later). Cosine is equal to sine but with a fase shift, which is not relevant in this context, it sounds exactly the same.

To generate the array of values of a sine wave we need the sampling rate, 41000, the frequency, which can be any value lower than 20.5 kHz by the [Nyquist frequency](https://en.wikipedia.org/wiki/Nyquist_frequency) (most people can't hear anything above 16 or 17 kHz anyway) and the duration for the sound sample.

With the duration and the sampling rate we can calculate the number of frames that the sample will have. With the number of frames and the duration we can generate an array with the timings of each frame, which in tur is fed into the cosine function multiplied by 2π and the frequency, this results in an array with all values of the sound signal. 

To hear it, first we have to turn it into a pygame sound array, which first has to be multiplied by the value of 32767, duplicated (for stereo mixer), transposed and turned into the int16 type. Then whe can use the function `make_sound` from pygame sndarray, the `.copy()` is necessary to make the array contiguous in memory. After that we can finally play the sound, careful with the volume, it will be at maximum! After that we simply wait for the duration of the sample an exit pygame.

<details>
  <summary>Generating the first sound sample</summary>
```python
import pygame as pg
import numpy as np

pg.init()
pg.mixer.init()

sampling_rate = 41000 # default value for the pygame mixer
frequency = 440 # [Hz]
duration = 1.5 # [s]
frames = int(duration*sampling_rate)
arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
sound = pg.sndarray.make_sound(sound.copy())
sound.play()
```
</details>

Great! Now we can do the same for all the notes in a piano keyboard.

## Generating samples for every key in a piano

But wait, wat are notes anyway? Simply put, notes are selected frequencys which often sound nice when played together. This may sound a bit weird, but the exact frequencies aren't that important, what matters most are the ratios between them. The most used ratio in western music is the [Twelfth root of two](https://en.wikipedia.org/wiki/Twelfth_root_of_two).

So, to generate samples for all the keys in a piano we just need a [list of all the notes](https://en.wikipedia.org/wiki/Piano_key_frequencies), conviniently I have listed them all in a text file: [noteslist.txt](https://github.com/FinFetChannel/Python_Synth/blob/main/noteslist.txt). Then we just need the frequency of the first note (16.35160 Hz) and the remaining frequencies can be calculated from it.

So, we can easily store a sample for each note in a dictionary. For the keys, we are going to use the caracters in a regular keyboard, after all, that's what we have to play here. The 108 keys can be subdivided into three groups of 36, since your keyboard probably does not have enough keys for all of them.

<details>
  <summary>Generating the first sound sample</summary>
```python
import pygame as pg
import numpy as np

pg.init()
pg.mixer.init()

def synth(frequency, duration=1.5, sampling_rate=41000):
    frames = int(duration*sampling_rate)
    arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
    sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())
    
    return sound


keylist = '123456789qwertyuioasdfghjklzxcvbnm,.'
notes_file = open("noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

keymod = '0-='
notes = {} # dict to store samples
freq = 16.3516 # start frequency

for i in range(len(noteslist)):
    mod = int(i/36)
    key = keylist[i-mod*36]+str(mod) 
    sample = synth(freq)
    notes[key] = [sample, noteslist[i], freq]
    notes[key][0].set_volume(0.33)
    notes[key][0].play()
    notes[key][0].fadeout(100)
    pg.time.wait(100)
    freq = freq * 2 ** (1/12)
    
pg.quit()
```
</details>
