# Spotiripper

## Usage

For the sake of speed, it's recommended to the scripts in python directly rather than building them.

### Spotiripper
The actual script recording music.

    python main.py <track URI>
    python main.py <track URL>
    python main.py <list.txt containing track URIs or URLs>
    python main.py <playlist URI>    (*)
    python main.py <playlist URL>    (*)
    python main.py <album URI>       (*)
    python main.py <album URL>       (*)
    python main.py <artist URI>      Downloads the artist's top 10 tracks. (*)
    python main.py <artist URL>      Downloads the artist's top 10 tracks. (*)

    (*) Note: requires setting Spotify Client ID and Client Secret keys.")
        export SPOTIPY_CLIENT_ID='yourclientid'")
        export SPOTIPY_CLIENT_SECRET='yourclientsecret'")

### Organizer
Move recorded files into an existing library structured hierarchically as Artist > Album > Track. 

    python organize.py -s <where_the_MP3_files_are> -l <library's parent folder>


### Waveform
Show the waveform of the first seconds of an MP3 file, this helps finding out how much to trim in case loud noises are
recorded at the beginning of the file.

    python waveform.py <track.mp3>


## External dependencies

### Spotify

It is better to use a paid account to get rid of ads that otherwise might be recorded.

Make sure "autoplay" is deactivated in the Settings. Otherwise, another random song is played after the one requested
and it might end up being recorded.

To download tracks (or a list or tracks) nothing more is necessary.

To download playlists, albums and artist's top tracks `spotiripper` needs to access the Spotify database to know what
tracks they contain. To do so, it is necessary to setup Client ID and Client Secret keys. They can be obtained
from [here](https://developer.spotify.com/dashboard/applications) and the keys can be set permanently to `~/.zshrc`
with:

````
echo "export LANG=\"en_US.UTF-8\"" >> ~/.zshrc
echo "export SPOTIPY_CLIENT_ID='yourclientid'" >> ~/.zshrc
echo "export SPOTIPY_CLIENT_SECRET='yourclientsecret'" >> ~/.zshrc
````

The first line makes sure you do not get the `UnicodeEncodeError` because the terminal cannot display some accented
character or the sound bar.


### Blackhole

It is necessary to route the audio stream internally and allow `spotiripper` to record internally. It can be downloaded
from [here](https://existential.audio/blackhole/) ([here](https://github.com/ExistentialAudio/BlackHole/wiki) is the
github for more documentation).

If you also want to listen to the music while recording you will need to create an aggregate output device (red circle).
In this case it is important to set the BlackHole virtual device bitrate to the same bitrate of the speakers (48kHz)
otherwise this nasty error appears at
random: `||PaMacCore (AUHAL)|| Error on line 2500: err='-10863', msg=Audio Unit: cannot do in current context`.

![alt text1](docs/audio_input.png "Input")
![alt text1](docs/audio_output.png "Output")

Make sure the volume slider in BlackHole is set to 1.0 (0.0dB) not to have an attenuated recording.

## Known bugs

Both pyaudio and sounddevice, sometimes, although the input device is set correctly to blackhole, pstart recording from
the microphone and then crash when attempting to close the stream.

Seems to have disappeared with the latest version of BlackHole.

````
Ripping track spotify:track:56wHTRjWMtWZ8RBKN1gcnj...                                                         
********************************************************************************
Portaudio version
(1246976, 'PortAudio V19.7.0-devel, revision unknown')

Recording file
tmp/tmp.wav

All devices
  0 DELL U2515H, Core Audio (0 in, 2 out)
* 1 BlackHole 2ch, Core Audio (2 in, 2 out)
  2 MacBook Pro Microphone, Core Audio (1 in, 0 out)
  3 MacBook Pro Speakers, Core Audio (0 in, 2 out)
  4 ZoomAudioDevice, Core Audio (2 in, 2 out)
  5 Speakers + BlackHole, Core Audio (0 in, 2 out)

Device that will be used:
Device #: 1
Channels: 2
Rate #: 48000
********************************************************************************
||PaMacCore (AUHAL)|| Warning on line 520: err=''!obj'', msg=Unknown Error
||PaMacCore (AUHAL)|| Warning on line 436: err=''!obj'', msg=Unknown Error
||PaMacCore (AUHAL)|| Error on line 1303: err='-10851', msg=Audio Unit: Invalid Property Value
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/Users/ste/.pyenv/versions/3.9.7/lib/python3.9/threading.py", line 973, in _bootstrap_inner
    self.run()
  File "/Users/ste/.pyenv/versions/3.9.7/lib/python3.9/threading.py", line 910, in run
    self._target(*self._args, **self._kwargs)
  File "/Users/ste/PycharmProjects/spotiripper/recorder_sounddevice.py", line 113, in _record
    with sd.InputStream(samplerate=self.rate,
  File "/Users/ste/.pyenv/versions/3.9.7/lib/python3.9/site-packages/sounddevice.py", line 1415, in __init__
    _StreamBase.__init__(self, kind='input', wrap_callback='array',
  File "/Users/ste/.pyenv/versions/3.9.7/lib/python3.9/site-packages/sounddevice.py", line 892, in __init__
    _check(_lib.Pa_OpenStream(self._ptr, iparameters, oparameters,
  File "/Users/ste/.pyenv/versions/3.9.7/lib/python3.9/site-packages/sounddevice.py", line 2741, in _check
    raise PortAudioError(errormsg, err)
sounddevice.PortAudioError: Error opening InputStream: Internal PortAudio error [PaErrorCode -9986]
````