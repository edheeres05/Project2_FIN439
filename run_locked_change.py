"""Optional post-experiment reproduction from a clean Git clone.
This verifies Git order and unchanged calculation inputs, not human authorship.
The original student UI export in the repository root is preserved separately.
"""
import argparse,subprocess,json,datetime
from pathlib import Path
from engine import review,ROOT,OPTIMIZERS

TRACKED=['engine.py','app.py','data','build_data.py','audit_data.py','requirements.txt','test_engine.py']
# Reporting and reproduction helpers were updated after the original UI run; the financial engine, inputs and tests remain frozen.
PREDICTION='ai-off-prediction.md'

def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True,stderr=subprocess.STDOUT).strip()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--baseline-commit',required=True);p.add_argument('--prediction-commit',required=True);args=p.parse_args()
    try:
        baseline=git('rev-parse','--verify',args.baseline_commit+'^{commit}');pred=git('rev-parse','--verify',args.prediction_commit+'^{commit}')
        if baseline==pred: raise ValueError('Prediction must be a separate later commit')
        git('merge-base','--is-ancestor',baseline,pred);git('merge-base','--is-ancestor',pred,'HEAD')
        # The student-authored prediction must be newly added and present at the prediction commit.
        if git('diff','--name-status',baseline,pred,'--',PREDICTION)!=f'A\t{PREDICTION}':raise ValueError('Prediction file must be newly added in the later commit')
        pred_text=git('show',f'{pred}:{PREDICTION}')
        if not pred_text.strip():raise ValueError('Prediction file is empty')
        if git('diff','--name-only',baseline,'--',*TRACKED):raise ValueError('Model, data or test code differs from frozen baseline')
        if git('status','--porcelain','--',*TRACKED):raise ValueError('Uncommitted model/data modifications')
    except (subprocess.CalledProcessError,FileNotFoundError,ValueError) as e:
        raise SystemExit('STOP: no experiment executed. '+str(e))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    base=review();changed=review(soxx_haircut=.10)
    record={'experiment':'SOXX-specific expected annual return haircut','old_value_pp':0,'new_value_pp':10,
      'baseline_commit':baseline,'baseline_commit_time':git('show','-s','--format=%cI',baseline),
      'prediction_commit':pred,'prediction_commit_time':git('show','-s','--format=%cI',pred),
      'prediction_file':PREDICTION,'execution_utc':now,'original':base,'changed':changed,
      'note':'Post-experiment reproduction only. Git order and unchanged calculation inputs verified locally. Original student UI execution evidence remains separate; authorship is not certified.'}
    out=ROOT/'outputs'/'locked-change-reproduction.json';out.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print('Wrote',out);print('Original:',base['recommendation']);print('Changed:',changed['recommendation'])
    for key,r in [('original',base),('changed',changed)]:
        for x in r['rows']:
            if x['portfolio'] in OPTIMIZERS: print(key,x['portfolio'],x['weights'],x['net_estimate'],x['volatility'],x['estimated_sharpe'],x['verdict'])
if __name__=='__main__':main()
