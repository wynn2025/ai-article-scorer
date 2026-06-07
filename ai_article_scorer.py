# AI Article Scorer v1.0.0
# 8-dimension article quality scoring, pure rule engine, no API needed
# Author: AI Tools Workshop

import re, sys, json, argparse
from pathlib import Path

class DimScore:
    def __init__(s, name, name_cn, score, weight):
        s.name=name; s.name_cn=name_cn; s.score=score; s.weight=weight
        s.details=[]; s.suggestions=[]
    @property
    def ws(s): return s.score*s.weight
    def to_dict(s):
        return dict(name=s.name_cn, score=round(s.score,1), weight=s.weight, details=s.details, suggestions=s.suggestions)

def grade_label(sc):
    if sc>=90: return 'S (best)'
    if sc>=80: return 'A (excellent)'
    if sc>=70: return 'B (good)'
    if sc>=60: return 'C (pass)'
    if sc>=50: return 'D (improve)'
    return 'F (fail)'

def extract_title(c):
    m=re.match(r'^#\s+(.+)',c)
    if m: return m.group(1).strip()
    return ''

def score_title(title):
    s=DimScore('title','title_quality',0,0.15)
    if not title: s.score=0; s.suggestions.append('Missing title!'); return s
    sc=50.0; ln=len(title)
    if 15<=ln<=35: sc+=15; s.details.append('Title length '+str(ln)+' optimal')
    elif 10<=ln<15 or 35<ln<=50: sc+=8
    else: s.suggestions.append('Title length '+str(ln)+' too short/long')
    if re.search(r'\d+',title): sc+=10; s.details.append('Has numbers')
    if re.search(r'[？?]',title): sc+=5; s.details.append('Has question')
    s.score=min(100,sc)
    if sc<60: s.suggestions.append('Weak title, add numbers/questions')
    return s

def score_opening(content):
    s=DimScore('opening','opening_hook',50,0.12)
    lines=[l.strip() for l in content.split(chr(10)) if l.strip()]
    opening=[]
    for line in lines[:8]:
        if not line.startswith('#') and len(line)>10:
            opening.append(line)
        if len(opening)>=3: break
    if not opening: s.score=20; s.suggestions.append('No opening'); return s
    sc=40.0
    if len(opening[0])<30: sc+=10; s.details.append('Short first sentence')
    s.score=min(100,sc)
    if sc<60: s.suggestions.append('Weak opening, hook reader')
    return s

def score_structure(content):
    s=DimScore('structure','structure',50,0.13); sc=50.0
    h2=len(re.findall(r'^## ',content,re.MULTILINE))
    if h2>=3: sc+=15; s.details.append(str(h2)+' H2 headers')
    elif h2>=1: sc+=8; s.suggestions.append('Need 3-8 H2')
    else: sc-=10; s.suggestions.append('No H2 headers!')
    bl=len(re.findall(r'^[-*+] ',content,re.MULTILINE))
    if bl>=3: sc+=10; s.details.append('Uses lists')
    else: s.suggestions.append('Use bullet lists')
    s.score=max(0,min(100,sc)); return s

def score_readability(content):
    s=DimScore('readability','readability',60,0.12); sc=60.0
    text=re.sub(r'^#+ .+$','',content,flags=re.MULTILINE)
    text=re.sub(r'```[\s\S]*?```','',text)
    sents=re.split(r'[。！？.!?]',text)
    sents=[x.strip() for x in sents if x.strip() and len(x.strip())>5]
    if not sents: s.score=30; return s
    avg=sum(len(x) for x in sents)/len(sents)
    if avg<=25: sc+=15; s.details.append('Avg sent '+str(round(avg,1)))
    elif avg>40: sc-=5; s.suggestions.append('Sentences too long')
    bold=len(re.findall(r'\*\*[^*]+\*\*',content))
    if bold>=5: sc+=10; s.details.append(str(bold)+' bold marks')
    elif bold==0: s.suggestions.append('Use **bold** for key points')
    s.score=min(100,sc); return s

def score_code_dim(content):
    s=DimScore('code','code_examples',0,0.10)
    blocks=re.findall(r'```(\w*)\n([\s\S]*?)```',content)
    inline=re.findall(r'`[^`]+`',content)
    if not blocks and not inline:
        s.score=40; s.details.append('No code (non-tech OK)'); return s
    sc=40.0
    if blocks:
        sc+=min(25,len(blocks)*8); s.details.append(str(len(blocks))+' blocks')
        langs=[l for l,_ in blocks if l]
        if langs: sc+=10; s.details.append('Langs: '+', '.join(set(langs)))
        else: s.suggestions.append('Add lang tags to code blocks')
    if inline: sc+=min(15,len(inline)*3)
    s.score=min(100,sc); return s

def score_seo(content,title=''):
    s=DimScore('seo','seo',50,0.10); sc=50.0
    links=re.findall(r'\[([^\]]+)\]\(([^)]+)\)',content)
    if links: sc+=10; s.details.append(str(len(links))+' links')
    tl=len(re.sub(r'[#\-*\s ]','',content))
    if tl>=2000: sc+=15; s.details.append('~'+str(tl)+' chars')
    s.score=min(100,sc); return s

def score_engagement(content):
    s=DimScore('engagement','engagement',30,0.10); sc=30.0
    for pat,pts,msg in [(r'(subscribe|follow)',15,'Follow CTA'),
        (r'(like|share|bookmark)',10,'Like CTA'),
        (r'(comment|reply)',10,'Comment CTA'),
        (r'(download|get|free)',8,'Resource CTA')]:
        if re.search(pat,content,re.IGNORECASE): sc+=pts; s.details.append(msg)
    s.score=min(100,sc)
    if sc<50: s.suggestions.append('Add CTA: follow+like+comment')
    return s

def score_originality(content):
    s=DimScore('originality','originality',50,0.08); sc=50.0
    data=re.findall(r'\d+(?:\.\d+)?(?:%|x|hours?|min|times?)',content)
    if len(data)>=5: sc+=10; s.details.append(str(len(data))+' data points')
    s.score=min(100,sc); return s

def score_article(content,title=''):
    if not title: title=extract_title(content)
    dims=[score_title(title),score_opening(content),score_structure(content),
          score_readability(content),score_code_dim(content),score_seo(content,title),
          score_engagement(content),score_originality(content)]
    tw=sum(d.weight for d in dims)
    total=sum(d.ws for d in dims)/tw
    wc=len(re.sub(r'[\s\n\r#\-*>()\[\]`]','',content)); rt=max(1,wc//400)
    class R: pass
    r=R(); r.file=''; r.total_score=round(total,1); r.grade=grade_label(total)
    r.dimensions=dims; r.word_count=wc; r.reading_time_minutes=rt
    r.top_suggestions=[]
    for d in dims: r.top_suggestions.extend('['+d.name_cn+'] '+sg for sg in d.suggestions)
    r.top_suggestions=r.top_suggestions[:6]
    return r

def format_report(r):
    L=['='*55,'  AI Article Quality Report','='*55,'']
    L.append('  Score: '+str(r.total_score)+'/100  Grade: '+r.grade)
    L.append('  Words: ~'+str(r.word_count)+'  Reading: ~'+str(r.reading_time_minutes)+'min')
    L.append('')
    filled=int(r.total_score/5)
    bar=chr(9608)*filled+chr(9617)*(20-filled)
    L.append('  ['+bar+'] '+str(r.total_score)+'%')
    L+=['','-'*55,'  Dimensions:','-'*55]
    for d in r.dimensions:
        bl=int(d.score/5)
        b=chr(9632)*bl+chr(9633)*(20-bl)
        L.append('  '+d.name_cn.ljust(14)+' ['+b+'] '+str(round(d.score,1)).rjust(5)+' (w'+str(int(d.weight*100))+'%)')
    L.append('')
    if any(d.details for d in r.dimensions):
        L+=['-'*55,'  Highlights:','-'*55]
        for d in r.dimensions:
            for det in d.details: L.append('  + ['+d.name_cn+'] '+det)
    if r.top_suggestions:
        L+=['-'*55,'  Suggestions:','-'*55]
        for i,sg in enumerate(r.top_suggestions,1): L.append('  '+str(i)+'. '+sg)
    L.append('='*55)
    return chr(10).join(L)

def main():
    p=argparse.ArgumentParser(description='AI Article Scorer')
    p.add_argument('input',help='Markdown file or dir')
    p.add_argument('--title','-t',help='Custom title')
    p.add_argument('--json',action='store_true',help='JSON output')
    p.add_argument('--batch',action='store_true',help='Batch mode')
    p.add_argument('--output','-o',help='Save report')
    args=p.parse_args()
    path=Path(args.input)
    if path.is_dir() and args.batch:
        results=[]
        for f in sorted(path.glob('**/*.md')):
            r=score_article(f.read_text(encoding='utf-8'),args.title)
            r.file=str(f); results.append(r)
        if args.json:
            print(json.dumps([dict(file=r.file,score=r.total_score,grade=r.grade,word_count=r.word_count) for r in results],ensure_ascii=False,indent=2))
        else:
            for r in results: print(r.file.rjust(40),str(r.total_score).rjust(5),r.grade)
    elif path.is_file():
        r=score_article(path.read_text(encoding='utf-8'),args.title)
        r.file=str(path)
        if args.json: print(json.dumps(dict(file=r.file,score=r.total_score,grade=r.grade,word_count=r.word_count,reading_time=r.reading_time_minutes,dimensions=[d.to_dict() for d in r.dimensions],top_suggestions=r.top_suggestions),ensure_ascii=False,indent=2))
        else: print(format_report(r))
        if args.output:
            Path(args.output).write_text(format_report(r),encoding='utf-8')
            print('Saved:',args.output)
    else: print('Not found:',path); sys.exit(1)

if __name__=='__main__': main()
