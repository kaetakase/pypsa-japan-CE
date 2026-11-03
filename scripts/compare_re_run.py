#!/usr/bin/env python3
"""Compare a newly executed case with the untouched reference results (not a solver)."""
import argparse,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def table(path):
 if not path.exists():raise FileNotFoundError(path)
 return pd.read_csv(path)

def load_run_dir(root,case,mode):
 name=case if mode=='full8760' else case+'_'+mode
 work=root/name/'results'
 hits=sorted(work.glob('*/results_csv'),key=lambda p:p.stat().st_mtime,reverse=True)
 if len(hits)!=1:raise RuntimeError(f'Expected exactly one optimization result directory in {work}, found {len(hits)}')
 return hits[0]

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('case',choices=['WG','REI','WG-CO2','REI-CO2','WG-SEP','REI-SEP'])
 ap.add_argument('--time-mode',choices=['full8760','rep4','rep8','rep10'],default='full8760')
 ap.add_argument('--work-root',type=Path,default=ROOT/'.work')
 ap.add_argument('--rtol',type=float,default=1e-4,help='Relative objective tolerance for solver comparison')
 a=ap.parse_args()
 name=a.case if a.time_mode=='full8760' else a.case+'_'+a.time_mode
 ref=ROOT/'reference_results'/name
 out=load_run_dir(a.work_root.resolve(),a.case,a.time_mode)
 r=table(ref/'cost_summary.csv');o=table(out/'cost_summary.csv')
 rm=dict(zip(r.category,pd.to_numeric(r.value,errors='coerce')))
 om=dict(zip(o.category,pd.to_numeric(o.value,errors='coerce')))
 ok=True
 for k in ['total_system_cost_including_carbon','total_investment_cost','total_variable_cost_including_carbon','actual_co2_intensity','annual_load_mwh']:
  v1=float(rm[k]);v2=float(om[k]); rel=abs(v1-v2)/max(abs(v1),1.0)
  hit=rel<=a.rtol
  print(f'{k:48s} ref={v1:.10g}, rerun={v2:.10g}, rel_diff={rel:.4g}', 'PASS' if hit else 'FAIL')
  ok &= hit
 rg=table(ref/'generation_summary.csv'); og=table(out/'generation_summary.csv')
 rdict=dict(zip(rg.carrier,rg.generation_mwh));odict=dict(zip(og.carrier,og.generation_mwh))
 print('Generation mix per-carrier differences (informational; LP degeneracy can move dispatch):')
 for carrier in sorted(set(rdict)|set(odict)):
  x=rdict.get(carrier,0);y=odict.get(carrier,0)
  if abs(x-y)>max(1e-3,1e-3*max(abs(x),abs(y))):print(' ',carrier,'ref',x,'rerun',y,'delta',y-x)
 print('RESULT:', 'PASS' if ok else 'FAIL', '(objective/cost/emissions/annual-load checks)')
 return 0 if ok else 1
if __name__=='__main__':sys.exit(main())
