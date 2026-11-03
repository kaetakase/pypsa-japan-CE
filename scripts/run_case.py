#!/usr/bin/env python3
"""Prepare and optionally execute each paper case without modifying tracked inputs.

Run from repository root:
    python scripts/run_case.py WG-CO2 --prepare-only
    python scripts/run_case.py WG-CO2 --run
    python scripts/run_case.py ALL --run
"""
import argparse, csv, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'cases.json').read_text(encoding='utf-8'))

def policy_case(c):
    # Important: the original model automatically ENABLES the intensity constraint
    # whenever the 'co2_intensity_tco2_per_mwh' key is present, regardless of the
    # preceding 'use_co2_intensity_constraint' flag. Therefore the intensity
    # parameter MUST be absent in unconstrained WG and REI scenarios.
    policy = {
        'carbon_price': str(c.get('carbon_price_jpy_per_tco2', 0)),
        'use_co2_intensity_constraint': 'TRUE' if c['co2_intensity_constraint'] else 'FALSE',
        'use_basic_mix_constraint': 'TRUE' if c['basic_mix_constraint'] else 'FALSE',
        'basic_mix_file': 'basic_mix_2040.csv',
    }
    if c['co2_intensity_constraint']:
        policy['co2_intensity_tco2_per_mwh'] = str(c['co2_intensity_tco2_per_mwh'])
    return policy

def prepare(name,work_root,overwrite=False,time_mode='full8760'):
    c=CONFIG['cases'][name]
    dirname=name if time_mode=='full8760' else f'{name}_{time_mode}'
    target=work_root/dirname
    if target.exists():
        if not overwrite:
            raise FileExistsError(f'{target} exists; use --overwrite explicitly')
        shutil.rmtree(target)
    target.mkdir(parents=True)
    shutil.copytree(ROOT/'input',target/'input')
    shutil.copyfile(ROOT/c['cost_file'],target/'input'/'technology_cost_2040.csv')
    with (target/'input'/'policy_2040.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['parameter','value']);w.writerows(policy_case(c).items())
    (target/'reproduction_metadata.json').write_text(json.dumps({
        'case':name,'time_mode':time_mode,
        'model_path':str(ROOT/CONFIG['original_model_file']),
        'case_configuration':c},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Prepared {name}: {target}')
    return target

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('case',choices=[*CONFIG['cases'],'ALL'])
    group=ap.add_mutually_exclusive_group()
    group.add_argument('--prepare-only',action='store_true',help='Stage inputs without optimizing (default)')
    group.add_argument('--run',action='store_true',help='Run PyPSA optimizer; resource intensive')
    ap.add_argument('--overwrite',action='store_true',help='Explicitly overwrite existing work subdirectory')
    ap.add_argument('--time-mode',choices=['full8760','rep4','rep8','rep10'],default=CONFIG['time_mode'],
                    help='Choose hourly resolution; paper main results use full8760')
    ap.add_argument('--work-root',type=Path,default=ROOT/'.work',help='Staging/output folder (gitignored)')
    args=ap.parse_args()
    args.work_root=args.work_root.resolve();args.work_root.mkdir(parents=True,exist_ok=True)
    names=list(CONFIG['cases']) if args.case=='ALL' else [args.case]
    for name in names:
        target=prepare(name,args.work_root,args.overwrite,time_mode=args.time_mode)
        if not args.run: continue
        env=os.environ.copy()
        env.update(CE_TIME_MODE=args.time_mode,CE_CASE_LABEL=name.lower().replace('-','_'))
        output_log=target/'run.log'
        print('Running',name,'log:',output_log)
        with output_log.open('w',encoding='utf-8') as log:
            result=subprocess.run([sys.executable,str(ROOT/CONFIG['original_model_file'])],cwd=target,
                                  env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f'{name} optimization failed (exit {result.returncode}); see {output_log}')
        print('Finished',name,'; results in:',target/'results')
    print('All requested scenarios prepared'+(' and run.' if args.run else '.'))

if __name__=='__main__': main()
