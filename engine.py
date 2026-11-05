import functools
import pandas as pd, numpy as np, re, math
from datetime import date
import os
D=os.environ.get("SB_DATA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))+"/"
courses=pd.read_csv(D+"Dataset/courses.csv"); mentors=pd.read_csv(D+"Dataset/mentors.csv")
students=pd.read_csv(D+"Dataset/students.csv"); asm=pd.read_csv(D+"Dataset/assessments.csv")
att=pd.read_csv(D+"Dataset/attendance.csv")
train=pd.read_csv(D+"Query Files/train.csv"); test=pd.read_csv(D+"Query Files/test.csv")
REF=pd.Timestamp("2025-01-15")
students['enrollment_date']=pd.to_datetime(students['enrollment_date'])
asm['due_date']=pd.to_datetime(asm['due_date']); asm['submitted_date']=pd.to_datetime(asm['submitted_date'])
att['date']=pd.to_datetime(att['date'])
S=students.merge(courses,left_on='course_enrolled',right_on='course_id',how='left').set_index('student_id')
asm_g={k:v for k,v in asm.groupby('student_id')}
att_g={k:v for k,v in att.groupby('student_id')}
W={'quiz':.20,'assignment':.30,'project':.25,'exam':.25}
def comp_avgs(sid):
    a=asm_g.get(sid); out={}
    for t in W:
        if a is None: out[t]=0.0; continue
        x=a[a.type==t]
        out[t]=100*x.scored.sum()/x.max_score.sum() if len(x) and x.max_score.sum()>0 else 0.0
    return out
def grade(sid):
    c=comp_avgs(sid); return sum(c[t]*W[t] for t in W)
def att_stats(sid):
    a=att_g.get(sid)
    if a is None: return dict(w=0.0,s=0.0,n=0,lab=0.0,lec=0.0,men=0.0)
    wt=np.where(a.session_type=='lab',1.5,1.0)
    cr=a.status.map({'present':1.0,'late':0.5,'absent':0.0}).values
    n=len(a)
    d=dict(w=100*(wt*cr).sum()/wt.sum(), s=100*cr.sum()/n, n=n)
    for k,nm in [('lab','lab'),('lec','lecture'),('men','mentoring')]:
        x=a[a.session_type==nm]
        d[k]=100*x.status.map({'present':1.0,'late':0.5,'absent':0.0}).sum()/len(x) if len(x) else 0.0
    return d
def alert(g,w):
    if g<50 or w<60: return 'Red'
    if g<65 or w<70: return 'Yellow'
    if g>=75 and w>=75: return 'Green'
    return 'Orange'
def weeks(sid): return (REF-S.loc[sid,'enrollment_date']).days/7
def expected(sid,floor=False):
    e=weeks(sid)/3
    if floor: e=math.floor(e)
    return min(S.loc[sid,'total_modules'],e)
def pstatus(cur,exp):
    if cur>=exp: return 1
    if cur>=exp-1: return 2
    if cur>=exp-3: return 3
    return 4
def letter(g):
    return 6 if g>=90 else 5 if g>=80 else 4 if g>=70 else 3 if g>=60 else 2 if g>=50 else 1

import functools
SIDS=list(S.index)
@functools.lru_cache(None)
def G(sid): return grade(sid)
@functools.lru_cache(None)
def A(sid): return att_stats(sid)
@functools.lru_cache(None)
def C(sid): return comp_avgs(sid)
def acode(sid): return {'Red':1,'Yellow':2,'Orange':3,'Green':4}[alert(G(sid),A(sid)['w'])]
def passing(sid): return S.loc[sid,'passing_grade']
def completion(sid): return 100*S.loc[sid,'current_module']/S.loc[sid,'total_modules']
def max_run(sid,fl=None):
    a=att_g[sid].sort_values('date',kind='stable'); best=cur=0
    for s in a.status:
        if s=='absent': cur+=1; best=max(best,cur)
        else: cur=0
    return best
def delay(sid):
    a=asm_g[sid]; return (a.submitted_date-a.due_date).dt.days.mean()
def r2(x): return round(float(x),2)
DOMAIN_KW=['grade','attendance','alert','progress','module','passing','completion','quiz','assignment','exam','delay','late','absent','weighted','letter','mentor','batch']
def UNMATCHED(ql):
    return None if any(k in ql for k in DOMAIN_KW) else OOS()
def OOS(): return dict(answerable=0,lookup_value=-1.0,rule_value=-1.0,final_answer=-1.0)
def R(l,r,f): return dict(answerable=1,lookup_value=float(l),rule_value=float(r),final_answer=float(f))
def course_of(q):
    best=None
    for n in courses.course_name:
        if n.lower() in q.lower() and (best is None or len(n)>len(best)): best=n
    return best
def course_students(cn): return [s for s in SIDS if S.loc[s,'course_name']==cn]
def batch_students(b): return [s for s in SIDS if S.loc[s,'batch']==b]
def solve(q):
    ql=q.lower()
    m=re.search(r'STU\d{4}',q); sid=m.group(0) if m else None
    bm=re.search(r'BATCH-\d{4}-[AB]',q); batch=bm.group(0) if bm else None
    cn=course_of(q)
    ismentor=re.search(r'MNT\d+',q)
    if sid is None and not batch and not cn and not ismentor and 'department' not in ql and 'mentor' not in ql:
        return OOS()
    # ---- course lookups
    if sid is None and cn and not batch and 'total modules' in ql:
        v=courses.set_index('course_name').loc[cn,'total_modules']; return R(v,0,v)
    if sid is None and cn and not batch and 'passing grade' in ql and 'students' not in ql.split('passing grade')[0][-30:]:
        if 'what is the passing grade' in ql or 'passing grade for' in ql:
            v=courses.set_index('course_name').loc[cn,'passing_grade']; return R(v,0,v)
    # ---- student-level
    if sid:
        g=G(sid); a=A(sid); c=C(sid); p=passing(sid)
        if 'assessment entries' in ql or 'assessments has' in ql or ('how many assessments' in ql):
            n=len(asm_g[sid]); return R(n,0,n)
        if 'attendance records' in ql:
            return R(a['n'],0,a['n'])
        if 'module number' in ql or 'current module' in ql:
            v=S.loc[sid,'current_module']; return R(v,0,v)
        if 'additional lecture' in ql:
            w=a['w']; 
            # sessions present k: (wp+k)/(wt+k)>=.75
            at=att_g[sid]; wt=np.where(at.session_type=='lab',1.5,1.0)
            cr=at.status.map({'present':1.0,'late':0.5,'absent':0.0}).values
            wp=(wt*cr).sum(); tot=wt.sum()
            k=max(0,math.ceil((0.75*tot-wp)/0.25-1e-9))
            return R(w,75,k)
        if 'escape the red' in ql:
            w=a['w']; return R(w,60,max(0,60-w))
        if 'minimum assignment average' in ql:
            X=c['quiz']*.2+c['project']*.25+c['exam']*.25
            f=(p-X)/.3
            return R(X,p,min(100,max(0,f)))
        if 'minimum exam' in ql:
            tgt=90 if ('a+' in ql or 'distinction' in ql) else 70
            X=c['quiz']*.2+c['assignment']*.3+c['project']*.25
            f=(tgt-X)/.25
            return R(X,tgt,min(100,max(0,f)))
        if 'green alert grade threshold' in ql:
            return R(g,75,max(0,75-g))
        if 'next letter grade' in ql:
            th=[50,60,70,80,90,100]; nx=next(t for t in th if t>g) 
            return R(g,nx,nx-g)
        if 'worst-performing component' in ql or 'weakest assessment' in ql:
            ws=min(W,key=lambda t:c[t]); rest=[t for t in W if t!=ws]
            f=sum(c[t]*W[t] for t in rest)/sum(W[t] for t in rest)
            return R(g,c[ws],f)
        if 'exam average and quiz average' in ql or 'exam-type average' in ql:
            return R(c['exam'],c['quiz'],c['exam']-c['quiz'])
        if 'project average compared' in ql:
            return R(c['project'],g,c['project']-g)
        if 'weighted and unweighted' in ql or 'session-type-weighted' in ql:
            return R(a['w'],a['s'],a['w']-a['s'])
        if 'submission delay' in ql:
            d=delay(sid); return R(d,0,d)
        if 'weeks behind' in ql:
            e=expected(sid); beh=max(0,e-S.loc[sid,'current_module'])
            return R(0 if beh==0 else beh,3,3*beh)
        if 'modules ahead or behind' in ql:
            e=expected(sid,True); d=S.loc[sid,'current_module']-e
            return R(S.loc[sid,'current_module'],e,d)
        if 'exactly 80%' in ql or '80%' in ql and 'alert color' in ql:
            ch=alert(g,80)!=alert(g,a['w']); return R(g,a['w'],int(ch))
        if 'increased by 10' in ql or 'boosted by 10' in ql:
            ch=alert(g+10,a['w'])!=alert(g,a['w']); return R(g,a['w'],int(ch))
        if 'consecutive' in ql:
            r=max_run(sid); return R(r,3,int(r>=3))
        if 'progress status' in ql or 'classify' in ql and 'progress' in ql:
            e=expected(sid); cur=S.loc[sid,'current_module']; return R(cur,e,pstatus(cur,e))
        if 'letter grade' in ql:
            return R(g,0,letter(g))
        if 'call priority' in ql:
            return R(acode(sid),0,acode(sid))
        if '75% minimum attendance' in ql or 'minimum attendance requirement' in ql:
            return R(a['w'],75,int(a['w']>=75))
        if 'passed' in ql:
            return R(g,p,int(g>=p))
        if 'grade points above or below' in ql:
            return R(g,p,g-p)
        if 'alert color' in ql or 'alert classification' in ql:
            return R(g,a['w'],acode(sid))
        if 'course completion' in ql or 'completion percentage' in ql:
            v=completion(sid); return R(v,0,v)
        if 'lab session attendance' in ql: return R(a['lab'],0,a['lab'])
        if 'unweighted' in ql or 'simple' in ql: return R(a['s'],0,a['s'])
        if 'weighted attendance' in ql or 'attendance rate' in ql: return R(a['w'],0,a['w'])
        for t in W:
            if f'{t} average' in ql or f'{t}-type' in ql: return R(c[t],0,c[t])
        if 'overall grade' in ql or 'composite' in ql: return R(g,0,g)
        return UNMATCHED(ql)
    # ---- aggregate level
    pool=None
    if batch and cn: pool=[s for s in batch_students(batch) if S.loc[s,'course_name']==cn]
    elif batch: pool=batch_students(batch)
    elif cn: pool=course_students(cn)
    if ismentor: pool=[s for s in SIDS if S.loc[s,'mentor_id']==ismentor.group(0)]
    if 'department' in ql:
        dep=re.search(r"department='([^']+)'",q).group(1)
        mids=set(mentors[mentors.department==dep].mentor_id); pool=[s for s in SIDS if S.loc[s,'mentor_id'] in mids]
    def col(x): return alert(G(x),A(x)['w'])
    if 'mentor with the most red' in ql:
        cnt=pd.Series([S.loc[s,'mentor_id'] for s in SIDS if col(s)=='Red']).value_counts(); v=cnt.max(); return R(v,0,v)
    if pool is None: return UNMATCHED(ql)
    n=len(pool)
    if 'how many students are in' in ql: return R(n,0,n)
    if 'red alert status' in ql or 'red-alert students are mentored' in ql:
        v=sum(col(s)=='Red' for s in pool); return R(v,0,v)
    for nm in ['green','yellow','orange','red']:
        if 'percentage of students' in ql and f"{nm} alert" in ql:
            v=sum(col(s)==nm.capitalize() for s in pool); return R(v,n,100*v/n)
    if "'at risk'" in ql and 'percentage' in ql:
        v=sum(pstatus(S.loc[s,'current_module'],expected(s))==4 for s in pool); return R(v,n,100*v/n)
    if 'currently passing' in ql:
        v=sum(G(s)>=passing(s) for s in pool); return R(v,n,100*v/n)
    if 'average course completion' in ql:
        v=np.mean([completion(s) for s in pool]); return R(v,0,v)
    if 'average weighted attendance of failing' in ql:
        f=[s for s in pool if G(s)<passing(s)]; v=np.mean([A(s)['w'] for s in f]) if f else 0; return R(len(f),0,v)
    if 'average weighted attendance' in ql:
        v=np.mean([A(s)['w'] for s in pool]); return R(v,0,v)
    if 'grade deficit' in ql or 'average shortfall' in ql:
        f=[s for s in pool if G(s)<passing(s)]; v=np.mean([passing(s)-G(s) for s in f]) if f else 0; return R(len(f),0,v)
    if 'average grade of red-alert' in ql:
        f=[s for s in pool if col(s)=='Red']; v=np.mean([G(s) for s in f]) if f else 0; return R(len(f),0,v)
    if 'grade of 70 or above' in ql:
        v=sum(G(s)>=70 for s in pool); return R(v,70,v)
    if 'weighted attendance below 60' in ql:
        v=sum(A(s)['w']<60 for s in pool); return R(v,60,v)
    if 'highest-grade student' in ql:
        b=max(pool,key=lambda s:G(s)); return R(G(b),0,A(b)['w'])
    if 'highest grade' in ql and '75%' in ql:
        ok=[s for s in pool if A(s)['w']>=75]; return R(len(ok),75,max(G(s) for s in ok) if ok else 0)
    if 'lowest weighted attendance' in ql:
        b=min(pool,key=lambda s:A(s)['w']); return R(A(b)['w'],0,G(b))
    if 'average grade' in ql:
        if batch and cn or ismentor:
            v=np.mean([G(s) for s in pool]) if pool else 0; return R(len(pool),0,v) if (batch and cn) else R(v,0,v)
        v=np.mean([G(s) for s in pool]); return R(v,0,v)
    return UNMATCHED(ql)


def student_metrics(sid):
    g=G(sid); a=A(sid); c=C(sid); cur=int(S.loc[sid,'current_module']); e=expected(sid)
    return {"student_id":sid,"name":S.loc[sid,'student_name'],"batch":S.loc[sid,'batch'],"course":S.loc[sid,'course_name'],
        "mentor_id":S.loc[sid,'mentor_id'],"grade":g,"quiz_avg":c['quiz'],"assignment_avg":c['assignment'],
        "project_avg":c['project'],"exam_avg":c['exam'],"passing_grade":int(passing(sid)),
        "weighted_attendance":a['w'],"simple_attendance":a['s'],"lab_attendance":a['lab'],"lecture_attendance":a['lec'],
        "mentoring_attendance":a['men'],"alert":alert(g,a['w']),"current_module":cur,
        "total_modules":int(S.loc[sid,'total_modules']),"expected_module":e,
        "progress":{1:"On Track",2:"Slightly Behind",3:"Behind",4:"At Risk"}[pstatus(cur,e)],
        "completion_pct":completion(sid),"letter":{1:"F",2:"D",3:"C",4:"B",5:"A",6:"A+"}[letter(g)],
        "max_consecutive_absences":int(max_run(sid)),"avg_submission_delay":float(delay(sid))}
@functools.lru_cache(None)
def all_metrics():
    return pd.DataFrame([student_metrics(s) for s in SIDS])
def group_metrics(batch=None,course_name=None,mentor_id=None,department=None):
    df=all_metrics()
    if batch: df=df[df.batch==batch]
    if course_name: df=df[df.course==course_name]
    if mentor_id: df=df[df.mentor_id==mentor_id]
    if department:
        mids=set(mentors[mentors.department==department].mentor_id); df=df[df.mentor_id.isin(mids)]
    return df
