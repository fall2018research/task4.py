from vid_to_aud import VidToAud
from vid_group_list import VidList
from wav2value import Wav2Value
import os
import librosa
import numpy as np
import  sys
import moviepy.editor as mp
import cv2


def gcc_phat(sig, refsig, fs=1, max_tau=None, interp=16):
    '''
    This function computes the offset between the signal sig and the reference signal refsig
    using the Generalized Cross Correlation - Phase Transform (GCC-PHAT)method.
  '''

    # make sure the length for the FFT is larger or equal than len(sig) + len(refsig)
    n = sig.shape[0] + refsig.shape[0]

    # Generalized Cross Correlation Phase Transform
    SIG = np.fft.rfft(sig, n=n)
    REFSIG = np.fft.rfft(refsig, n=n)
    R = SIG * np.conj(REFSIG)

    cc = np.fft.irfft(R / np.abs(R), n=(interp * n))

    max_shift = int(interp * n / 2)
    max_shift = int(interp * n / 2)
    if max_tau:
        max_shift = np.minimum(int(interp * fs * max_tau), max_shift)

    cc = np.concatenate((cc[-max_shift:], cc[:max_shift + 1]))

    # find max cross correlation index
    shift = np.argmax(np.abs(cc)) - max_shift

    tau = shift / float(interp * fs)

    return tau, cc

def main():

    files = os.listdir("./")
    for f in files:
       if f.lower()[-3:] == "mp4":
            # print "processing", f
            inFile = f
            cap = cv2.VideoCapture(inFile)
            fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
            _, image = cap.read()
            outVideo = cv2.VideoWriter(f[:-3] + "avi", fourcc, 30, (image.shape[1],image.shape[0]))
            count =1
            while (1):
              ret, image = cap.read()
              flag = 1
              if  flag:
                  image_h, image_w, _ = image.shape
                  print("checked for shape".format(image.shape))
                  cv2.putText(image, "Frame: {0}" .format(count), (10, 230), 6, 2, (255, 0, 255), 3)
                  outVideo.write(image)
                  cv2.imshow('image',image)
                  count+=1
            outFile = f[:-3] + "wav"
            clip2 = mp.VideoFileClip(f)
            clip = mp.VideoFileClip(f).subclip(0,clip2.duration)
            clip.audio.write_audiofile(f[:-3] + "wav")
            y, sr = librosa.load(inFile, sr=None, mono=False)
            y_8k = librosa.resample(y,sr,2000)
            librosa.output.write_wav(outFile, y_8k, 2000)


    filesTotal = []
    video_path = './'
    output_name_1 = 'body.wav'

    dirs = os.listdir("./")

    for k in dirs:
        if k.lower()[-3:] == "wav" and k.find("body")== -1  :
           

            print(k)
    #    if f.lower()[-3:] == "wav"   :
    #      inFile = f
    #obj_vid_list = VidList(8, video_path)
    #obj_vid_list.extract_video_list('templist.txt')
    #obj_vid_name = obj_vid_list.get_file_name('templist.txt')
    #VidToAud(video_path + video_name_1,video_path + output_name_1).extract_audio()
    #VidToAud(video_path + video_name_2, video_path + output_name_2).extract_audio()
    # extract wav file to int16 value. Use the same channel(0-left, 1-right) to do the cc later
            rate1, data1 = Wav2Value(video_path + output_name_1).get_wav_para()
            rate2, data2 = Wav2Value(video_path + k).get_wav_para()
            offset, _ = gcc_phat(data1[0:10*rate1, 0], data2[0:10*rate2, 0]);
            offset = (offset/44100)*30
            filesTotal.append(offset)

    #print(data1[0:5760000, 0])
    #Wav2Value(video_path + output_name_1).plot_wav(0)
    for x in filesTotal:
        print(x)
main()
