The created software is an audio file analyzer that allows comparing two songs, an original and a cover version, and evaluating the similarity between their vocals. It can analyze the mel spectrogram of each song to check for the presence of harmonic components (corresponding to the fundamental frequencies of the musical notes) and percussive components (corresponding to the beats and other percussive noises) in the vocals. Additionally, the software uses the harmonic-percussive separation technique (HPSS) to separate the harmonic and percussive components of each song and calculate the Euclidean distance between them.

Based on these analyses, the software reports the spectral, harmonic, and percussive distances between the songs and offers suggestions to improve the cover version, such as adjusting elements such as pitch, timbre, and dynamics of the vocal, as well as other mixing elements, such as equalization and ambiance. The software presents the information in a simple and intuitive graphical interface, with plots that show the differences between the songs in terms of frequency and time, as well as a description of the analysis results.

To use, just download the latest version of python on python site
And do those pip installs: 

librosa
numpy
matplot.lib

And finally exec the file PY

In the future i will update this and make a executable file without need it pip
