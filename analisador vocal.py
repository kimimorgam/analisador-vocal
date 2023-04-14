import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, StringVar, Frame, Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def carregar_arquivo(tipo):
    arquivo = filedialog.askopenfilename(title=f'Selecione o arquivo de áudio ({tipo})', filetypes=[('Arquivos de áudio', '*.mp3 *.wav *.flac')])
    return arquivo

def analisar_audio(arquivo):
    audio, sr = librosa.load(arquivo, sr=None, mono=True)
    mel_spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
    tamanho = 20783  # tamanho padrão para todas as matrizes
    if mel_spectrogram.shape[1] < tamanho:
        mel_spectrogram = np.pad(mel_spectrogram, ((0, 0), (0, tamanho - mel_spectrogram.shape[1])), mode='constant')
    else:
        mel_spectrogram = mel_spectrogram[:, :tamanho]
    return mel_spectrogram

def comparar_audios(original, cover):
    distancia = np.linalg.norm(original - cover)
    return distancia

def comparar_vocais(original, cover):
    original_harm, original_perc = librosa.effects.hpss(original)
    cover_harm, cover_perc = librosa.effects.hpss(cover)
    distancia_harm = np.linalg.norm(original_harm - cover_harm)
    distancia_perc = np.linalg.norm(original_perc - cover_perc)
    return distancia_harm, distancia_perc

def plotar_graficos(original, cover):
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    img1 = librosa.display.specshow(librosa.power_to_db(original, ref=np.max), ax=ax[0], x_axis='time', y_axis='mel')
    img2 = librosa.display.specshow(librosa.power_to_db(cover, ref=np.max), ax=ax[1], x_axis='time', y_axis='mel')
    ax[0].set_title('Original')
    ax[1].set_title('Cover')
    return fig

def analisar_e_comparar():
    original_arquivo = carregar_arquivo('Original')
    cover_arquivo = carregar_arquivo('Cover')

    original = analisar_audio(original_arquivo)
    cover = analisar_audio(cover_arquivo)

    distancia_spectral = comparar_audios(original, cover)
    distancia_harm, distancia_perc = comparar_vocais(original, cover)

    if original_arquivo == cover_arquivo:
        descricao_var.set('Por favor, selecione arquivos diferentes para comparar.')
        resultado_var.set('')
    elif distancia_harm < 10 and distancia_perc < 10:
        descricao_var.set('Os vocais do cover são bastante semelhantes aos do original. Poucas melhorias são necessárias.')
        resultado_var.set(f'Distância Espectral: {distancia_spectral:.2f}, Distância Harmônica: {distancia_harm:.2f}, Distância Percussiva: {distancia_perc:.2f}')
    else:
        descricao_var.set(
            f'Os espectrogramas de mel mostram uma distância de {distancia_spectral:.2f}, enquanto a distância vocal '
            f'(de acordo com a análise harmônica e percussiva) é de {distancia_harm:.2f} e {distancia_perc:.2f}, respectivamente. '
            f'Para melhorar o cover, é possível ajustar elementos como tom, timbre e dinâmica do vocal, '
            f'assim como outros elementos da mixagem, como equalização e ambiência.')
        resultado_var.set(f'Distância Espectral: {distancia_spectral:.2f}, Distância Harmônica: {distancia_harm:.2f}, Distância Percussiva: {distancia_perc:.2f}')
    
    fig = plotar_graficos(original, cover)
    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

janela = Tk()
janela.title('Comparador de Áudio por Kimi Morgam')
janela.state('zoomed')

resultado_var = StringVar()
resultado_var.set('')

descricao_var = StringVar()
descricao_var.set('')

botao_analisar = Button(janela, text='Analisar e Comparar', command=analisar_e_comparar)
botao_analisar.place(relx=0.5, rely=0.1, anchor='center')

resultado_label = Label(janela, textvariable=resultado_var)
resultado_label.place(relx=0.5, rely=0.2, anchor='center')

descricao_label = Label(janela, textvariable=descricao_var, wraplength=janela.winfo_screenwidth() * 0.6, justify='left')
descricao_label.place(relx=0.5, rely=0.3, anchor='center')

frame_graficos = Frame(janela)
frame_graficos.place(relx=0.5, rely=0.6, anchor='center')

janela.mainloop()
