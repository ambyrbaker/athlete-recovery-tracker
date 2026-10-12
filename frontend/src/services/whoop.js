// Only the local backend talks to WHOOP or handles OAuth credentials.
export const WHOOP_CONNECT_URL = '/api/whoop/connect';
const metricKeys = ['recovery_score', 'hrv_rmssd_milli', 'resting_heart_rate', 'spo2_percentage', 'skin_temp_celsius'];
export class WhoopError extends Error {
  constructor(kind) { super(kind); this.name = 'WhoopError'; this.kind = kind; }
}
export async function fetchWhoopRecovery({signal} = {}) {
  const controller = new AbortController();
  const abort = () => controller.abort();
  if (signal?.aborted) controller.abort();
  signal?.addEventListener('abort', abort, {once:true});
  const timeout = setTimeout(abort, 25000);
  try {
    const response = await fetch('/api/whoop/recovery', {
      signal:controller.signal, headers:{Accept:'application/json'}, cache:'no-store',
    });
    const body = await response.json().catch(() => null);
    if (response.status === 401) {
      const detail = typeof body?.detail === 'string' ? body.detail.toLowerCase() : '';
      throw new WhoopError(detail.includes('not connected') || detail.includes('token is missing') ? 'disconnected' : 'expired');
    }
    if (!response.ok) throw new WhoopError('error');
    if (body?.message === 'No WHOOP recovery data available') return null;
    if (!body || typeof body !== 'object' || !metricKeys.some(key => Object.hasOwn(body,key))) throw new WhoopError('error');
    // Whitelist values; never forward arbitrary backend fields or error text to the UI.
    return {
      date:typeof body.date === 'string' && Number.isFinite(Date.parse(body.date)) ? body.date : null,
      ...Object.fromEntries(metricKeys.map(key => [key, typeof body[key] === 'number' && Number.isFinite(body[key]) ? body[key] : null])),
    };
  } catch (error) {
    if (signal?.aborted) throw error;
    throw error instanceof WhoopError ? error : new WhoopError('error');
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener('abort', abort);
  }
}
