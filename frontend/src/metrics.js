export const dateKey = (date = new Date()) => `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
export function dashboardMetrics(data, today = dateKey()) {
  const end = new Date(`${today}T12:00:00`);
  const start = new Date(end); start.setDate(start.getDate()-((start.getDay()+6)%7));
  const weekly = data.training.filter(r=>r.date>=dateKey(start)&&r.date<=today);
  const wellness = data.wellness.filter(r=>r.date>=dateKey(start)&&r.date<=today);
  const average = key => wellness.length ? wellness.reduce((s,r)=>s+r[key],0)/wellness.length : null;
  const days = Array.from({length:14},(_,i)=>{const d=new Date(end);d.setDate(d.getDate()-13+i);const key=dateKey(d);const logs=data.wellness.filter(r=>r.date===key);return {date:key,load:data.training.filter(r=>r.date===key).reduce((s,r)=>s+r.duration_minutes*r.rpe,0),sleep:logs.length?logs.reduce((s,r)=>s+r.sleep_hours,0)/logs.length:null};});
  return {weekly,load:weekly.reduce((s,r)=>s+r.duration_minutes*r.rpe,0),duration:weekly.reduce((s,r)=>s+r.duration_minutes,0),soreness:average('soreness'),stress:average('stress'),days};
}
