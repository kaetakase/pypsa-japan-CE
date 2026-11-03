#!/usr/bin/env python3
"""Static verification of repository inputs and archived reference results.
No solver installation or 8760h rerun is performed.
"""
from pathlib import Path
import csv, hashlib, io, json, math, sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
CASES=json.loads((ROOT/'cases.json').read_text(encoding='utf-8'))['cases']
EXPECTED_COST={'WG':6.8,'REI':6.5,'WG-CO2':11.8,'REI-CO2':8.3,'WG-SEP':12.1,'REI-SEP':10.9}
SHADOW_EXPECTED={'WG-CO2':3.6,'REI-CO2':2.5,'WG-SEP':4.0,'REI-SEP':3.5}

def get(case,table):
    p=ROOT/'reference_results'/case/(table+'.csv')
    if not p.exists(): return None
    return pd.read_csv(p)

def value(case,key):
    d=get(case,'cost_summary')
    row=d.loc[d['category']==key,'value']
    if row.empty: raise AssertionError(f'{case}: missing {key}')
    return float(row.iloc[0])

def main():
    errors=[]
    inventory=ROOT/'reference_results/source_files.csv'
    manifest=pd.read_csv(inventory)
    for row in manifest.itertuples(index=False):
        p=ROOT / row.published_path
        if not p.exists(): errors.append(f'missing reference: {p}')
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=row.sha256:errors.append(f'modified reference: {p}')
    for case, cfg in CASES.items():
        d=get(case,'model_settings'); kv=dict(zip(d['parameter'],d['value']))
        if str(kv.get('TIME_MODE')).lower()!='full8760':errors.append(f'{case}: wrong time mode')
        co2=str(kv.get('USE_CO2_INTENSITY_CONSTRAINT')).lower()=='true'
        sep=str(kv.get('USE_BASIC_MIX_CONSTRAINT')).lower()=='true'
        if co2!=cfg['co2_intensity_constraint']:errors.append(f'{case}: co2 flag mismatch')
        if sep!=cfg['basic_mix_constraint']:errors.append(f'{case}: basic mix flag mismatch')
        cost=value(case,'total_system_cost_including_carbon')/1e12
        reported=EXPECTED_COST[case]
        if round(cost,1)!=reported:errors.append(f'{case}: paper cost {reported} vs {cost:.3f}')
        intensity=value(case,'actual_co2_intensity')
        if co2 and abs(intensity-0.04)>2e-5:errors.append(f'{case}: co2 intensity exceeds 0.04: {intensity}')
        annualload=value(case,'annual_load_mwh')
        if abs(annualload-1_090_416_652)>1:errors.append(f'{case}: annual load mismatch: {annualload}')
        shadow=get(case,'co2_shadow_price_summary')
        if co2:
            cost_co2=float(shadow['shadow_price_jpy_per_tco2'].iloc[0])/10000
            if round(cost_co2,1)!=SHADOW_EXPECTED[case]:errors.append(f'{case}: shadow price mismatch {cost_co2}')
        print(f'{case:<8s} total={cost:8.5f} trillion JPY (paper {reported:.1f}); intensity={intensity:.6f}; load={annualload/1e6:.3f} TWh')
    for mode,report in [('rep4',10.1),('rep8',9.5),('rep10',9.7)]:
        case='REI-CO2_'+mode
        cost=value(case,'total_system_cost_including_carbon')/1e12
        print(f'{case:<14s} representative-week cost={cost:.5f} (paper {report:.1f})')
        if round(cost,1)!=report:errors.append(f'{case}: Figure 3 mismatch')
    # input checks: 9 areas and exactly 8760 timeseries rows
    for name in ('load','solar_pu','wind_on_pu','wind_off_pu','hydro_pu','geothermal_pu','biomass_pu','nuc_pu'):
        p=ROOT/'input'/(name+'_2040.csv');df=pd.read_csv(p)
        if df.shape[0]!=8760 or df.shape[1]!=10:errors.append(f'{p.name}: invalid dimensions {df.shape}')
        if df.isna().any().any():errors.append(f'{p.name}: missing data')
    if errors:
        for e in errors:print('ERROR',e,file=sys.stderr)
        print('FAILED:',len(errors),'issue(s)',file=sys.stderr);return 1
    print('PASS: reference CSV integrity, model flags, annual load, paper costs, CO2 shadows, basic input dimensions.')
    print('LIMITATION: this is NOT proof that source code reproduces the numerical results; full model rerun is still required.')
    return 0
if __name__=='__main__':sys.exit(main())
