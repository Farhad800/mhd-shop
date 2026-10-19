# usage: python3 src/build_p3.py prices.json   (prices.json = {"p01":{"price":5000,"note":""},...})
import json,sys
N=json.load(open('src/batch2-names.json'));pr=json.load(open(sys.argv[1]))
out=[]
for k in sorted(N):
    v=pr.get(k) or {};p=v.get('price')
    if not p: continue
    cat,ar,ku,en=N[k];i=int(k[1:])
    out.append('{id:%d,img:"img/m%02d.webp",fit:"ct",cat:"%s",price:%d,n:%s}'%(300+i,i,cat,int(p),json.dumps({"ar":ar,"ku":ku,"en":en},ensure_ascii=False)))
open('js/p3.js','w').write('P.push(\n'+',\n'.join(out)+(',\n' if out else '')+');\n')
print(len(out),'priced of',len(N))
