"""Volume final do vídeo: limitador, ganho até -14 LUFS e limitador de pico. Entrada audio/mix.wav, saída audio/final_novo.wav."""
import subprocess, re, pathlib
p=pathlib.Path(__file__).parent; SRC=p/"mix.wav"; T1=p/"lim1.wav"; OUT=p/"final_novo.wav"
def run(*a): return subprocess.run(["ffmpeg","-loglevel","error","-y",*a],check=True)
def medir(f):
    r=subprocess.run(["ffmpeg","-nostats","-i",str(f),"-af","ebur128=peak=true","-f","null","-"],capture_output=True,text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS",r)[-1]),float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS",r)[-1])
run("-i",str(SRC),"-af","alimiter=limit=0.5:level=0",str(T1))
I,_=medir(T1); g=-14.0-I
for _ in range(3):
    run("-i",str(T1),"-af",f"volume={g:.2f}dB,alimiter=limit=0.80:level=0","-ar","48000","-c:a","pcm_s16le",str(OUT))
    I2,pk=medir(OUT)
    if abs(I2+14.0)<0.15: break
    g+=-14.0-I2
print(f"final: {I2:.1f} LUFS | pico {pk:.1f} dBFS | ganho {g:.2f} dB")
