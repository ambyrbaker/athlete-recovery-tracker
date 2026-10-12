import React, {useEffect, useId, useState} from 'react';
import {fetchWhoopRecovery, WHOOP_CONNECT_URL} from '../services/whoop';
import './whoop-recovery.css';

const metrics = [
  ['recovery_score','Recovery','%',0],
  ['hrv_rmssd_milli','HRV','ms',1],
  ['resting_heart_rate','Resting heart rate','bpm',0],
  ['spo2_percentage','SpO₂','%',1],
  ['skin_temp_celsius','Skin temperature','°C',1],
];
const messages = {
  disconnected:'WHOOP is not connected. Connect your account to see recovery data.',
  expired:'Your WHOOP session has expired or is no longer valid. Reconnect your account to continue.',
  error:'Unable to load WHOOP recovery. Please try again.',
  empty:'No WHOOP recovery data is available yet. Sync your device and check again.',
};
export default function WhoopRecovery() {
  const titleId = useId();
  const [attempt,setAttempt] = useState(0);
  const [state,setState] = useState({status:'loading',data:null});
  useEffect(() => {
    const controller = new AbortController();
    setState({status:'loading',data:null});
    fetchWhoopRecovery({signal:controller.signal}).then(data => {
      if (!controller.signal.aborted) setState({status:data?'ready':'empty',data});
    }).catch(error => {
      if (!controller.signal.aborted) setState({status:error.kind || 'error',data:null});
    });
    return () => controller.abort();
  },[attempt]);
  const {status,data} = state;
  const reconnect = status === 'expired' || status === 'disconnected';
  return <section className="whoop-recovery" aria-labelledby={titleId} aria-busy={status==='loading'}>
    <div className="whoop-heading">
      <div><h2 id={titleId}>WHOOP Recovery</h2>{data?.date && <time dateTime={data.date}>Latest record · {new Date(data.date).toLocaleString(undefined,{month:'short',day:'numeric',year:'numeric',hour:'numeric',minute:'2-digit'})}</time>}</div>
      <button className="text-button" disabled={status==='loading'} onClick={()=>setAttempt(value=>value+1)} aria-label="Refresh WHOOP recovery">{status==='loading'?'Loading…':'Refresh'}</button>
    </div>
    <div role="status" aria-live="polite">
      {status==='loading' ? <p className="whoop-message">Loading recovery data…</p> : status==='ready' ? <>
        <dl className="whoop-metrics">{metrics.map(([key,label,unit,precision])=><div key={key}><dt>{label}</dt><dd>{data[key]===null ? <span aria-label="Not available">—</span> : <>{data[key].toFixed(precision)}<span className="whoop-unit">{unit}</span></>}</dd></div>)}</dl>
        {metrics.some(([key])=>data[key]===null)&&<p className="whoop-note">Unavailable measurements are shown as —.</p>}
      </> : <p className="whoop-message">{messages[status]}</p>}
    </div>
    {reconnect && <div className="whoop-connect"><a className="button secondary" href={WHOOP_CONNECT_URL} target="_blank" rel="noopener noreferrer">{status==='expired'?'Reconnect WHOOP':'Connect WHOOP'} ↗</a><p className="whoop-note">Opens in a new tab. After connecting, return here and select Refresh.</p></div>}
  </section>;
}
