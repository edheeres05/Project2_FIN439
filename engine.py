"""Six-ETF research engine. No trading, live allocation, or claimed historical alpha."""
from datetime import date
from functools import lru_cache
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parent
TICKERS=('VOO','QQQ','SOXX','SCHD','BIL','BND')
BENCH=np.array([.50,0,0,0,.10,.40])
SNAPSHOT_DATE=date(2026,11,24) # source capture; review is end of day
OBSERVATION_DATE=date(2026,10,30) # final trading session of October
DATA_LIMIT_DAYS=45
RETURN_HASH='33294b3122e0990303672b4cca389a1462930a160a214662875bf4361ead4378'
RF_HASH='a21726cfad77a51aec46c7ffedf9121175efee453c687e14aaa5e6ffbef1ebc5'
RISK_FREE=.0437
MIN_VOL='Minimum volatility'
MAX_SHARPE='Maximum estimated Sharpe'
OPTIMIZERS=(MIN_VOL,MAX_SHARPE)
EPS=1e-10


def validate_returns(p):
    if list(p.columns)!=list(TICKERS) or p.shape!=(60,6):
        raise ValueError('Expected 60 completed months and six ETFs in the declared order')
    expected=pd.date_range('2021-11-30','2026-10-31',freq=pd.offsets.MonthEnd())
    if not p.index.equals(expected):
        raise ValueError('Incorrect, missing, duplicate or non-month-end date')
    arr=p.to_numpy(dtype=float)
    if not np.isfinite(arr).all() or (arr<=-100).any() or (abs(arr)>100).any():
        raise ValueError('Invalid monthly return percent; review units and source')
    return p/100


def load_returns(path=None,*,verify=True):
    path=Path(path) if path else ROOT/'data'/'monthly_returns_pct.csv'
    raw=path.read_bytes()
    if verify and hashlib.sha256(raw).hexdigest()!=RETURN_HASH:
        raise ValueError('Return snapshot checksum mismatch; stop and reconcile source')
    p=pd.read_csv(path,index_col=0,parse_dates=True)
    return validate_returns(p)


def load_rf():
    path=ROOT/'data'/'risk_free.json'
    if hashlib.sha256(path.read_bytes()).hexdigest()!=RF_HASH:
        raise ValueError('Treasury reference checksum mismatch')
    rf=json.loads(path.read_text(encoding='utf-8'))
    if rf['series']!='DGS3MO' or float(rf['annual_percent'])/100!=RISK_FREE:
        raise ValueError('Treasury reference inconsistent with model')
    return rf


@lru_cache(maxsize=1)
def grid():
    """All nonnegative six-asset 5%-increment portfolios, exactly 100% invested."""
    def parts(left,n):
        if n==1: yield (left,)
        else:
            for i in range(left+1):
                for tail in parts(left-i,n-1): yield (i,)+tail
    arr=np.array(list(parts(20,6)),float)/20
    arr.setflags(write=False)
    return arr


def estimate_from(r,haircut=0.,soxx_haircut=0.):
    if len(r)<2 or not 0<=haircut<=.50 or not 0<=soxx_haircut<=.50:
        raise ValueError('Insufficient returns or invalid equity haircut')
    mu=r.mean().to_numpy()*12
    mu[:4]-=haircut
    mu[2]-=soxx_haircut
    cov=r.cov().to_numpy()*12
    if not np.isfinite(cov).all() or np.any(np.diag(cov)<=0) or np.min(np.linalg.eigvalsh(cov))<-1e-9:
        raise ValueError('Invalid annual covariance; no optimization')
    return mu,cov


def estimates(window=60,equity_haircut=0.,soxx_haircut=0.):
    if window not in (36,48,60): raise ValueError('Choose 36, 48 or 60 monthly returns')
    return estimate_from(load_returns().tail(window),equity_haircut,soxx_haircut)


def metrics(weights,mu,cov,current,cost_bps):
    w=np.atleast_2d(np.asarray(weights,float));current=np.asarray(current,float)
    gross=w@mu
    traded=np.abs(w-current).sum(axis=1)
    cost=traded*cost_bps/10000
    net=(1-cost)*(1+gross)-1
    variance=np.einsum('ij,jk,ik->i',w,cov,w)
    if np.min(variance)<-1e-9: raise ValueError('Negative portfolio variance')
    vol=np.sqrt(np.maximum(variance,0))
    return gross,net,vol,traded/2,cost


def optimize(mu,cov,current,cost_bps,target,reserve,vol_limit,turnover_limit,prior_turnover,risk_free):
    w=grid();g,n,v,t,c=metrics(w,mu,cov,current,cost_bps)
    good=(n>=target-EPS)&(w[:,4]>=reserve-EPS)&(v<=vol_limit+EPS)&(t+prior_turnover<=turnover_limit+EPS)
    good &= v>EPS
    sharpe=np.divide(n-risk_free,v,out=np.full_like(v,-np.inf),where=v>EPS)
    ids=np.flatnonzero(good)
    choices={}
    if ids.size:
        # Tie policy: lower vol, higher net, lower turnover, then grid order.
        m=ids[np.lexsort((ids,t[ids],-n[ids],v[ids]))[0]]
        s=ids[np.lexsort((ids,t[ids],v[ids],-sharpe[ids]))[0]]
        choices={MIN_VOL:w[m],MAX_SHARPE:w[s]}
    return choices,good,(g,n,v,t,c,sharpe)


def frontier_points(good,metrics_arrays):
    """Non-dominated feasible grid points; sorted by risk, maximizing net return."""
    _,n,v,_,_,_=metrics_arrays
    ids=np.flatnonzero(good)
    ids=ids[np.lexsort((-n[ids],v[ids]))]
    out=[];best=-np.inf
    for i in ids:
        if n[i]>best+EPS:
            out.append({'volatility':float(v[i]),'net_return':float(n[i])});best=n[i]
    return out


def review(*,window=60,cost_bps=10.,target=.06,reserve=.05,vol_limit=.15,
           turnover_limit=.25,prior_turnover=0.,drawdown=0.,current=None,
           equity_haircut=0.,soxx_haircut=0.,decision_date='2026-11-24',risk_free=RISK_FREE,include_frontier=False):
    params=np.asarray([cost_bps,target,reserve,vol_limit,turnover_limit,prior_turnover,drawdown,equity_haircut,soxx_haircut,risk_free],float)
    if not np.isfinite(params).all() or (params<0).any(): raise ValueError('Nonnegative finite parameters required')
    if cost_bps>100 or any(x>1 for x in (target,reserve,vol_limit,turnover_limit,prior_turnover,drawdown)) or risk_free>.30 or equity_haircut>.50 or soxx_haircut>.50:
        raise ValueError('Scenario exceeds allowed bounds')
    if window not in (36,48,60): raise ValueError('Choose 36, 48 or 60 monthly returns')
    current=BENCH.copy() if current is None else np.asarray(current,float)
    if current.shape!=(6,) or not np.isfinite(current).all() or (current<0).any() or abs(current.sum()-1)>EPS:
        raise ValueError('Six nonnegative pre-trade weights must sum to 100%')
    asof=pd.Timestamp(decision_date).date()
    if pd.isna(asof): raise ValueError('Invalid decision date')
    if asof<SNAPSHOT_DATE: raise ValueError('No review before the source snapshot became available on November 24, 2026')
    r=load_returns();rf=load_rf()
    stale=(asof-OBSERVATION_DATE).days>DATA_LIMIT_DAYS
    mu,cov=estimate_from(r.tail(window),equity_haircut,soxx_haircut)
    momentum=float((1+r.VOO.tail(12)).prod()-1)
    paused=drawdown>=.15-EPS or momentum<=0
    choices,good,arr=optimize(mu,cov,current,cost_bps,target,reserve,vol_limit,turnover_limit,prior_turnover,risk_free)
    iv=1/np.sqrt(np.diag(cov));iv/=iv.sum()
    portfolios={'Equal weight':np.full(6,1/6),'Inverse volatility':iv,'Benchmark':BENCH.copy(),**choices}
    rows=[]
    for name,weights in portfolios.items():
        g,n,v,t,c=(float(z[0]) for z in metrics(weights,mu,cov,current,cost_bps))
        fail=[]
        if n<target-EPS: fail.append('Net return target')
        if weights[4]<reserve-EPS: fail.append('Minimum BIL reserve')
        if v>vol_limit+EPS: fail.append('Volatility ceiling')
        if t+prior_turnover>turnover_limit+EPS: fail.append('Rolling turnover ceiling')
        operational=[]
        if stale: operational.append('Stale data')
        if paused: operational.append('Signal/drawdown pause')
        rows.append({'portfolio':name,'weights':dict(zip(TICKERS,map(float,weights))),
            'gross_estimate':g,'net_estimate':n,'volatility':v,'estimated_sharpe':(n-risk_free)/v if v>EPS else None,
            'one_way_turnover':t,'rolling_turnover':t+prior_turnover,'trading_cost':c,
            'equity_weight':float(weights[:4].sum()),'numerical_verdict':'FAIL' if fail else 'PASS',
            'verdict':'FAIL' if fail or operational else 'PASS','failed_rules':fail+operational})
    reasons=[]
    if stale: reasons.append('Month-end return data older than 45 days')
    if drawdown>=.15-EPS: reasons.append('Account drawdown at or above 15%')
    if momentum<=0: reasons.append('Nonpositive trailing 12-month VOO total return')
    if not choices: reasons.append('No feasible grid allocation')
    status='STOP / NO NEW RISK' if reasons else 'PILOT: paper trading only'
    out={'decision_date':str(asof),'snapshot_date':str(SNAPSHOT_DATE),'data_end':'2026-10-31',
         'last_trading_session':str(OBSERVATION_DATE),'data_age_days':(asof-OBSERVATION_DATE).days,
         'source':'PortfoliosLab monthly total returns, rounded 0.01 percentage point','return_file_sha256':RETURN_HASH,
         'window_returns':window,'risk_free':risk_free,'risk_free_source':rf,'risk_free_scenario':bool(abs(risk_free-RISK_FREE)>EPS),
         'cost_bps':cost_bps,'target':target,'reserve':reserve,'vol_limit':vol_limit,'turnover_limit':turnover_limit,
         'prior_turnover':prior_turnover,'drawdown':drawdown,'equity_haircut':equity_haircut,'soxx_haircut':soxx_haircut,
         'pretrade_weights':dict(zip(TICKERS,map(float,current))),'signal_value':momentum,
         'stale':stale,'paused':paused,'grid_count':len(grid()),'feasible_grid_count':int(good.sum()),
         'rows':rows,'asset_annual_arithmetic_means':dict(zip(TICKERS,map(float,mu))),
         'asset_annual_volatilities':dict(zip(TICKERS,map(float,np.sqrt(np.diag(cov))))),
         'recommendation':status,'stop_reasons':reasons,'live_allocation':0.0}
    if include_frontier:
        out['frontier']=frontier_points(good,arr)
        _,n,v,_,_,_=arr
        ids=np.flatnonzero(good)
        # All feasible points, not a randomly sampled chart.
        out['feasible_points']=[{'volatility':float(v[i]),'net_return':float(n[i])} for i in ids]
    return out


def stress_suite(**base):
    """Only published exploratory scenarios. A separate student-locked input is never auto-run."""
    cases={'Base':{},'Trading costs 30 bps':{'cost_bps':30.},'Trading costs 50 bps':{'cost_bps':50.},
      'Equity annual means minus 2 pp':{'equity_haircut':.02},'36-month window':{'window':36},'48-month window':{'window':48},
      'BIL reserve floor 10%':{'reserve':.10},'Turnover ceiling 10%':{'turnover_limit':.10},
      'Volatility ceiling 5%':{'vol_limit':.05},'Drawdown 15%':{'drawdown':.15},
      ('Treasury proxy +1 pp' if base.get('risk_free',RISK_FREE)<=.29 else 'Treasury proxy -1 pp'): {'risk_free':base.get('risk_free',RISK_FREE)+(.01 if base.get('risk_free',RISK_FREE)<=.29 else -.01)}}
    return {name:review(**{**base,**kw,'include_frontier':False}) for name,kw in cases.items()}


def historical_path(r,weights,cost_bps=10.,current=BENCH):
    """Retrospective fixed-target annual rebalance, with drift and both-side costs.
    Returns net of modeled initial/annual trades. NOT a mandate-enforced strategy backtest.
    """
    w=np.asarray(weights,float);hold=np.asarray(current,float).copy();wealth=1.;points=[1.];trades=[]
    for i,values in enumerate(r.to_numpy()):
        if i%12==0:
            traded=float(np.abs(hold-w).sum());cost=traded*cost_bps/10000
            wealth*=1-cost;hold=w.copy();trades.append({'month':str(r.index[i].date()),'one_way_turnover':traded/2,'cost_fraction':cost})
        growth=hold*(1+values);factor=float(growth.sum())
        if factor<=0: raise ValueError('Portfolio wealth nonpositive')
        wealth*=factor;hold=growth/factor;points.append(wealth)
    p=np.array(points);dd=p/np.maximum.accumulate(p)-1
    returns=p[1:]/p[:-1]-1
    return {'dates':[str((r.index[0]-pd.offsets.MonthEnd()).date()),*[str(x.date()) for x in r.index]],
      'wealth':p.tolist(),'drawdown':dd.tolist(),'cagr':float(p[-1]**(12/len(r))-1),
      'annualized_realized_volatility':float(returns.std(ddof=1)*np.sqrt(12)),
      'max_month_end_drawdown':float(dd.min()),'total_return':float(p[-1]-1),'trades':trades}


def retrospective_diagnostics(result):
    r=load_returns()
    current=np.array(list(result['pretrade_weights'].values()))
    return {row['portfolio']:historical_path(r,list(row['weights'].values()),result['cost_bps'],current)
      for row in result['rows'] if row['portfolio'] in ('Benchmark',*OPTIMIZERS)}


def chronological_check():
    """Research-only chronological split; later revised data, not untouched prospective proof."""
    r=load_returns();train=r.iloc[:36];test=r.iloc[36:]
    # 3-month Treasury CMT 4.67%, 2024-10-30 (US Treasury table).
    historical_rf=.0467
    mu,cov=estimate_from(train)
    choices,good,_=optimize(mu,cov,BENCH,10.,.06,.05,.15,.25,0.,historical_rf)
    candidates={'Benchmark':BENCH,**choices}
    paths={k:historical_path(test,w) for k,w in candidates.items()}
    return {'training_start':str(train.index[0].date()),'training_end':str(train.index[-1].date()),
      'evaluation_start':str(test.index[0].date()),'evaluation_end':str(test.index[-1].date()),
      'historical_rf':historical_rf,'rf_date':'2024-10-30','training_feasible_grid_count':int(good.sum()),
      'weights':{k:dict(zip(TICKERS,map(float,w))) for k,w in candidates.items()},'paths':paths,
      'limitation':'Revised snapshot, chosen split examined now; not a locked holdout or point-in-time backtest. Annual fixed-target rebalancing, no signal/mandate enforcement during evaluation.'}
