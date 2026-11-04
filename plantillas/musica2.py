import numpy as np, sys, wave
# genera pista instrumental original: semilla define tonalidad, tempo, progresión e instrumento
seed=int(sys.argv[1]); dur=float(sys.argv[2]); out=sys.argv[3]
rng=np.random.default_rng(seed); sr=44100
key=int(rng.integers(50,64)); bpm=int(rng.integers(80,126)); beat=60/bpm


progs=[[0,5,3,4],[0,3,5,4],[5,3,0,4],[0,4,5,3],[3,0,4,5],[0,5,2,4],[0,2,5,3],[4,5,3,0]]; prog=progs[int(rng.integers(0,8))]
minor=[0,2,3,5,7,8,10]
def f(m): return 440*2**((m-69)/12)
t=np.arange(int(sr*dur))/sr; mix=np.zeros_like(t)
def tone(freq,start,length,kind,amp):
    i0=int(start*sr); n=int(length*sr)
    if i0>=len(t): return
    n=min(n,len(t)-i0); tt=np.arange(n)/sr
    if kind==0: w=np.sin(2*np.pi*freq*tt)+.3*np.sin(4*np.pi*freq*tt)
    elif kind==1: w=np.sign(np.sin(2*np.pi*freq*tt))*.35
    else: w=2*(tt*freq%1)-1; w*=.3
    env=np.minimum(1,tt/0.02)*np.exp(-tt*(2.5 if kind else 1.2))
    mix[i0:i0+n]+=w*env*amp
bar=4*beat; inst=int(rng.integers(0,3))
for b in range(int(dur/bar)+1):
    deg=prog[b%4]; root=key+minor[deg]-12
    for k in (0,2,4):
        m=key+minor[(deg+k)%7]+(12 if deg+k>6 else 0)
        tone(f(m),b*bar,bar,0,.07)                      # pad
    for s in range(4): tone(f(root-12),b*bar+s*beat,beat*.9,2,.18)  # bajo
    for s in range(8):                                   # arpegio
        m=key+12+minor[(deg+[0,2,4,2,0,4,2,4][(s+seed)%8])%7]
        tone(f(m),b*bar+s*beat/2,beat/2,inst if inst else 1,.06)
    for s in range(4):                                   # pulso suave
        i0=int((b*bar+s*beat)*sr); n=min(int(.08*sr),len(t)-i0)
        if n>0: mix[i0:i0+n]+=rng.normal(0,1,n)*np.exp(-np.arange(n)/sr*60)*(.12 if s%2 else .05)
fade=int(sr*1.2); mix[-fade:]*=np.linspace(1,0,fade); mix[:int(sr*.3)]*=np.linspace(0,1,int(sr*.3))
mix=mix/np.max(np.abs(mix))*.7
d=(mix*32767).astype(np.int16); st=np.stack([d,d],1)
with wave.open(out,'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes())
