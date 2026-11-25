"""Reproduce baseline, stress cases and retrospective diagnostics for reviewers."""
import json
from pathlib import Path
from engine import review,stress_suite,OPTIMIZERS,retrospective_diagnostics,chronological_check
ROOT=Path(__file__).resolve().parent

def main():
    out=ROOT/'outputs';out.mkdir(exist_ok=True)
    r=review(include_frontier=True);cases=stress_suite();diag=retrospective_diagnostics(r);chron=chronological_check()
    data={'baseline.json':{k:v for k,v in r.items() if k!='feasible_points'},'stress_summary.json':{k:{'decision':v['recommendation'],'count':v['feasible_grid_count'],'rows':[x for x in v['rows'] if x['portfolio'] in OPTIMIZERS]} for k,v in cases.items()},'historical_diagnostics.json':diag,'chronological_check.json':chron}
    for filename,content in data.items():(out/filename).write_text(json.dumps(content,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    lines=['FIN 439 Project 2 | November 24, 2026 frozen research review','60 completed monthly total returns, November 2021–October 2026.','Treasury proxy: 4.37%; source available Nov 24, 2026 after 3:16 CST.',f"Signal: {r['signal_value']:.2%}; feasible {r['feasible_grid_count']:,}/{r['grid_count']:,}",'Portfolio | net annual estimate | annual volatility | estimated Sharpe | one-way turnover | verdict']
    for x in r['rows']:
        lines.append(f"{x['portfolio']} | {x['net_estimate']:.2%} | {x['volatility']:.2%} | {x['estimated_sharpe']:.3f} | {x['one_way_turnover']:.2%} | {x['verdict']}")
        if x['portfolio'] in OPTIMIZERS:lines.append('  '+', '.join(f'{t} {w:.0%}' for t,w in x['weights'].items() if w>0))
    lines.extend([r['recommendation']+'; 0% live capital','Research-only; the chronological diagnostic is not a true holdout.','Independent human precommit/cold run/recordings not generated.'])
    (out/'visible-summary.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines))
if __name__=='__main__':main()
