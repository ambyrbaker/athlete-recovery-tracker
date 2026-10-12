import React, {useEffect, useRef, useState} from 'react';
import './opening.css';

const VISIT_KEY = 'recovery-tracker:intro-seen';

export default function OpeningScreen({children}) {
  const [visible, setVisible] = useState(() => {
    try { return sessionStorage.getItem(VISIT_KEY) !== 'yes'; }
    catch { return true; }
  });
  const dashboard = useRef(null);
  const skip = useRef(null);
  const played = useRef(visible);

  function finish() {
    try { sessionStorage.setItem(VISIT_KEY, 'yes'); } catch { /* Storage is optional. */ }
    setVisible(false);
  }

  useEffect(() => {
    if (!visible) {
      if (played.current) {
        const heading = dashboard.current?.querySelector('h1');
        heading?.setAttribute('tabindex', '-1');
        heading?.focus({preventScroll: true});
        played.current = false;
      }
      return;
    }
    skip.current?.focus({preventScroll: true});
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const timer = window.setTimeout(finish, reducedMotion.matches ? 900 : 2400);
    const onKey = event => { if (event.key === 'Escape') finish(); };
    const onMotion = event => { if (event.matches) finish(); };
    window.addEventListener('keydown', onKey);
    reducedMotion.addEventListener('change', onMotion);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      clearTimeout(timer);
      window.removeEventListener('keydown', onKey);
      reducedMotion.removeEventListener('change', onMotion);
      document.body.style.overflow = previousOverflow;
    };
  }, [visible]);

  return <>
    <div ref={dashboard} inert={visible} aria-hidden={visible ? true : undefined}
      className={visible ? 'dashboard-stage intro-pending' : 'dashboard-stage'}>
      {children}
    </div>
    {visible && <section className="opening-screen" aria-labelledby="opening-title">
      <div className="opening-glow" aria-hidden="true"/>
      <svg className="opening-trail" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <path className="trail-shadow" d="M -100 690 C 170 690 210 260 535 235 C 940 202 1000 715 1540 365"/>
        <path className="trail-line" pathLength="1" d="M -100 690 C 170 690 210 260 535 235 C 940 202 1000 715 1540 365"/>
      </svg>
      <div className="opening-title-wrap">
        <div className="opening-rule" aria-hidden="true"/>
        <h1 id="opening-title">Athlete Recovery<span>&amp; Rehab Tracker</span></h1>
      </div>
      <button ref={skip} className="opening-skip" onClick={finish}>Skip intro <span aria-hidden="true">↗</span></button>
    </section>}
  </>;
}
