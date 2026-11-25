"""Independent arithmetic/definition checks against separately reported source values.
No network. Values are documented in docs/data-provenance.md; no auto-correction.
"""
import json
from pathlib import Path
import pandas as pd
from engine import load_returns,load_rf,TICKERS,RETURN_HASH
ROOT=Path(__file__).resolve().parent
# Calendar-year total-return columns on the same provider's source pages; these
# are separately reported checksums, not inputs to the engine (percentage points).
ANNUAL={
 'VOO':[-18.17,26.32,24.98,17.82], 'QQQ':[-32.58,54.86,25.58,20.77],
 'SOXX':[-35.09,67.12,12.92,40.74], 'SCHD':[-3.26,4.54,11.66,4.34],
 'BIL':[1.40,4.94,5.19,4.15], 'BND':[-13.11,5.65,1.38,7.08]}
# Digrin Sep/Oct adjusted price pairs, captured 2026-11-24, not model inputs.
DIGRIN={'VOO':(700.86,694.81),'QQQ':(739.77,690.49),'SOXX':(189.55,157.17),
 'SCHD':(32.53,35.78),'BIL':(91.07,91.39),'BND':(69.65,71.56)}
# Second publisher confirmations on two material inputs.
CROSSCHECKS=[{'asset':'BND','month':'2026-10','reference_pct':2.37,
 'source':'https://www.lazyportfolioetf.com/etf/vanguard-total-bond-market-bnd/','definition':'USD one-month nominal reinvested return, period ending Oct 31, 2026'},
 {'asset':'SOXX','month':'2026-10','reference_pct':-17.1,
 'source':'https://chartrow.com/quote/soxx/monthly-returns','definition':'Dividend/split-adjusted monthly total return, 0.1 pp display rounding'}]

def audit():
    r=load_returns();annual=[]
    for year in range(2022,2026):
        vals=((1+r[r.index.year==year]).prod()-1)*100
        for t in TICKERS:
            expected=ANNUAL[t][year-2022];diff=float(vals[t]-expected)
            annual.append({'asset':t,'year':year,'compounded_monthly_pct':float(vals[t]),'published_annual_pct':expected,'difference_pp':diff,'within_rounding_tolerance':abs(diff)<=.10})
    month=[]
    for t,(a,b) in DIGRIN.items():
        alt=100*(b/a-1);primary=float(r.iloc[-1][t]*100)
        month.append({'asset':t,'month':'2026-10','primary_total_return_pct':primary,'alternate_adjusted_price_ratio_pct':alt,'difference_pp':alt-primary,'status':'REVIEW: not interchangeable' if abs(alt-primary)>.10 else 'agrees within 0.10 pp display tolerance'})
    cross=[]
    for q in CROSSCHECKS:
        p=float(r.loc['2026-10-31',q['asset']]*100);cross.append({**q,'primary_pct':p,'difference_pp':p-q['reference_pct']})
    return {'monthly_shape':list(r.shape),'return_hash':RETURN_HASH,'rf':load_rf(),'annual_checks':annual,'october_price_ratio_checks':month,'independent_publisher_checks':cross,
      'note':'Same-provider annual compounding checks detect transcription errors but are not independent source verification. Digrin discrepancy for BND is not spliced into the series; independent one-month return agrees with primary. Providers may share upstream data. No redistribution rights confirmed.'}
if __name__=='__main__':
    out=audit();(ROOT/'outputs'/'data-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('Annual checks within tolerance:',sum(v['within_rounding_tolerance'] for v in out['annual_checks']),'/',len(out['annual_checks']))
    print('Maximum absolute annual difference (pp):',max(abs(x['difference_pp']) for x in out['annual_checks']))
    print('October cross-checks:')
    for x in out['october_price_ratio_checks']: print(x['asset'],round(x['difference_pp'],3),x['status'])
