import numpy as np, onnxruntime as ort, cv2, json, sys
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
U='/root/.claude/uploads/93de00e5-afde-5394-90c6-9342519909ac/'
sess=ort.InferenceSession('/root/models/isnet.onnx',providers=['CPUExecutionProvider']);inp=sess.get_inputs()[0].name
def mask(im):
    x=np.asarray(im.convert('RGB').resize((1024,1024),Image.BILINEAR)).astype(np.float32)/255.-0.5
    o=sess.run(None,{inp:x.transpose(2,0,1)[None]})[0][0,0];o=(o-o.min())/(o.max()-o.min()+1e-8)
    return np.asarray(Image.fromarray((o*255).astype(np.uint8)).resize(im.size,Image.BILINEAR)).copy()
D=json.load(open('data.json'))['rows']
split={'p17':'L','p18':'R','p20':'L','p21':'R','p24':'L','p25':'R','p43':'L','p44':'R','p45':'T','p46':'B','p47':'T','p48':'B'}
only=sys.argv[1:]
MULTI={'p10','p11','p17','p18','p36','p45','p46','p47','p48','p09'};THR={'p10':50,'p11':50,'p17':60,'p18':60,'p45':60,'p46':60,'p47':60,'p48':60,'p09':60}
for r in D:
    if only and r['id'] not in only: continue
    src=Image.open(U+r['img']+'-image.jpg').convert('RGB');W,H=src.size
    s=split.get(r['id']);box=(0,0,W,H)
    if s=='L':box=(0,0,W//2,H)
    if s=='R':box=(W//2,0,W,H)
    if s=='T':box=(0,0,W,H//2)
    if s=='B':box=(0,H//2,W,H)
    im=src.crop(box);m=mask(im)
    t=THR.get(r['id'],128)
    if t<128: m=np.where(m>t,np.maximum(m,200),m).astype(np.uint8)
    if r['id']=='p28':
        x0,y0,x1,y1=317,67,840,1517
        hsv=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2HSV).astype(int);A=np.asarray(im).astype(np.float32)
        keep=((hsv[...,0]>=85)&(hsv[...,0]<=125)&(hsv[...,1]>60))|((hsv[...,1]<55)&(hsv[...,2]>150));keep[:275]=True
        keep=cv2.morphologyEx(keep.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3)))
        wood=1-keep.astype(np.float32)
        wood=cv2.GaussianBlur(wood,(9,9),0)[...,None];g=A.mean(2,keepdims=True)
        A=A*(1-wood)+243*wood;im=Image.fromarray(np.clip(A,0,255).astype(np.uint8))
        m=np.zeros_like(m);cv2.rectangle(m,(x0,y0),(x1+x0*0+0,y1),255,-1)
        m[:]=0;m[67:1517,317:840]=255
    GR={'p17':(150,60,595,1580),'p18':(30,60,520,1580)}
    if r['id'] in GR:
        x0,y0,x1,y1=GR[r['id']];arr=np.asarray(im)[:,:,::-1].copy();gm=np.zeros(m.shape,np.uint8)
        gm[y0:y1,x0:x1]=cv2.GC_PR_BGD;gm[(m>128)&(gm==cv2.GC_PR_BGD)]=cv2.GC_PR_FGD
        if r['id'] in ('p17','p18','p28'): gm[y0:y1,x0:x1]=cv2.GC_PR_FGD
        bg_=np.zeros((1,65));fg_=np.zeros((1,65))
        cv2.grabCut(arr,gm,(x0,y0,x1-x0,y1-y0) if False else None,bg_,fg_,6,cv2.GC_INIT_WITH_MASK)
        m=np.where((gm==1)|(gm==3),255,0).astype(np.uint8);m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5)))
    HP={'p10':[(398,395),(410,370),(430,330),(455,300),(490,275),(520,265),(536,268),(535,285),(510,300),(480,318),(455,345),(430,380),(412,405)],
        'p11':[(292,402),(330,404),(380,392),(440,375),(500,355),(530,340),(548,335),(552,350),(540,362),(500,375),(450,395),(400,415),(340,440),(300,447)]}
    if r['id'] in HP:
        q=np.zeros_like(m);cv2.fillPoly(q,[np.array([[x*2,y*2] for x,y in HP[r['id']]],np.int32)],255)
        m=np.where(m>128,255,0).astype(np.uint8);m=np.maximum(m,q);r['_multi']=1
    if r['id']=='p40':
        hsv=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2HSV).astype(int);yl=(hsv[...,0]>=18)&(hsv[...,0]<=38)&(hsv[...,1]>90);yl[600:]=False;m[cv2.dilate(yl.astype(np.uint8),np.ones((15,15)))>0]=0
        top=np.zeros_like(m,bool);top[:565,:]=True;top[:565,560:655]=False;m[top]=0
    b=(m>128).astype(np.uint8);n,lab,st,_=cv2.connectedComponentsWithStats(b)
    if n>1:
        ar=st[1:,cv2.CC_STAT_AREA];
        ks=[1+i for i in range(len(ar)) if ((r['id'] in MULTI or r.get('_multi')) and ar[i]>0.08*ar.max()) or ar[i]==ar.max()]
        keep=cv2.dilate(np.isin(lab,ks).astype(np.uint8),np.ones((9,9)))>0;m[~keep]=0
    mm=(m>128).astype(np.uint8)*255;cn,_=cv2.findContours(mm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);fill=np.zeros_like(mm);cv2.drawContours(fill,cn,-1,255,-1);m=np.maximum(m,fill)
    a=np.asarray(im).astype(np.float32);pm=m>200
    if pm.sum()>500:
        lo=np.percentile(a[pm],1,axis=0);hi=np.percentile(a[pm],99,axis=0)
        st_=np.clip((a-lo)/np.maximum(hi-lo,1)*255,0,255);a=a*0.5+st_*0.5
    e=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
    e=ImageEnhance.Brightness(e).enhance(1.04);e=ImageEnhance.Contrast(e).enhance(1.06);e=e.filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=2))
    if r['id']=='p49': e=e.rotate(-55,expand=True,fillcolor=(255,255,255));m=np.asarray(Image.fromarray(m).rotate(-55,expand=True))
    al=Image.fromarray(m).filter(ImageFilter.GaussianBlur(0.8));rg=e.copy();rg.putalpha(al)
    bb=al.point(lambda v:255 if v>20 else 0).getbbox();rg=rg.crop(bb)
    W2,H2=800,1000;pw,ph=rg.size;sc=min(W2*0.8/pw,H2*0.8/ph);rg=rg.resize((max(1,int(pw*sc)),max(1,int(ph*sc))),Image.LANCZOS);pw,ph=rg.size
    x=(W2-pw)//2;y=int(H2*0.1)+(int(H2*0.8)-ph)//2
    bg=Image.new('RGB',(W2,H2),(255,255,255));sh=Image.new('L',(W2,H2),0);ImageDraw.Draw(sh).ellipse((x+pw*0.1,y+ph-14,x+pw*0.9,y+ph+18),fill=90)
    bg.paste((200,200,205),(0,0),sh.filter(ImageFilter.GaussianBlur(14)));bg.paste(rg,(x,y),rg)
    bg.save('hi_%s.jpg'%r['id'],quality=90);print(r['id'],end=' ',flush=True)
