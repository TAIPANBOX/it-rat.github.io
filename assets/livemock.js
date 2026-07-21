/* IT-RAT v2 - livemock.js: interactive design mocks of the two iOS apps,
   running as real DOM in the page.
   - Pocket: a full iPhone (Runs, Run detail with a real slide-to-arm breaker,
     Budgets with an org/team/agent drill-in, Agents flagged by behaviour,
     Pairing, Device, Alerts, plus an unlooped Live Activity surface) and an
     Apple Watch (Face, Fleet, Runs, Kill, Killed). Numbers tick, the segmented
     control filters, the breaker drags, the tab bar and side steps switch
     screens, and a kill from the wrist updates the phone.
   - Sphere: real iOS screenshots in an iPhone and Watch frame, navigated
     by the side steps and an on-frame switcher.
   Honest label: design mocks, not app captures (Pocket screens are drawn;
   Sphere screens are real captures). Vanilla, no deps.
   LiveMock.pocket(mountEl, stepsEl); LiveMock.sphere(mountEl, stepsEl); */
(function(){
"use strict";
const reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
const $=(el,q)=>el.querySelector(q);
const $$=(el,q)=>[...el.querySelectorAll(q)];
const f2=n=>(Math.round(n*100)/100).toFixed(2);
function clock(){const d=new Date();return d.getHours()+":"+String(d.getMinutes()).padStart(2,"0");}

/* ---------------- shared styles ---------------- */
const CSS=`
.lm-wrap{display:flex;gap:26px;align-items:flex-start;flex-wrap:wrap}
/* ---- iPhone frame ---- */
.lm-phone{position:relative;width:min(320px,80vw);aspect-ratio:588/1240;border-radius:46px;
  background:linear-gradient(180deg,#20262f,#12161c);padding:5px;flex:0 0 auto;
  box-shadow:0 2px 0 rgba(255,255,255,.06) inset,0 34px 80px -30px rgba(0,0,0,.9),
    0 0 60px -18px color-mix(in srgb, var(--accent) 26%, transparent)}
.lm-scr{position:absolute;inset:5px;border-radius:41px;overflow:hidden;background:#070A0F;
  display:flex;flex-direction:column;font-family:var(--font-t)}
.lm-island{position:absolute;top:10px;left:50%;transform:translateX(-50%);width:88px;height:24px;
  background:#000;border-radius:15px;z-index:40}
.lm-sb{display:flex;justify-content:space-between;align-items:center;padding:11px 20px 2px;font-size:11px;font-weight:600;color:var(--fg);flex:0 0 auto}
.lm-sb .r{display:flex;gap:5px;align-items:center}
.lm-body{flex:1;position:relative;overflow:hidden;min-height:0}
.lm-view{position:absolute;inset:0;display:none;flex-direction:column;overflow:hidden}
.lm-view.on{display:flex;animation:lmSlide .34s cubic-bezier(.2,.6,.2,1)}
@keyframes lmSlide{from{opacity:0;transform:translateX(var(--lmdir,10px))}to{opacity:1;transform:none}}
.lm-scroll{flex:1;overflow-y:auto;padding:2px 14px 16px;min-height:0;overscroll-behavior:contain;touch-action:pan-y;cursor:grab}
.lm-scroll:active{cursor:grabbing}
.lm-h1{font-family:var(--font-d);font-weight:800;font-size:23px;letter-spacing:-.02em;margin:10px 0 0}
.lm-chip{display:inline-flex;align-items:center;gap:6px;font-family:var(--font-m);font-size:9.5px;
  color:var(--dim);background:var(--panel);border:1px solid var(--line);padding:4px 9px;border-radius:999px;margin-top:9px}
.lm-chip .k{width:6px;height:6px;border-radius:50%;background:var(--mint);box-shadow:0 0 8px var(--mint)}
/* hero burn instrument */
.lm-hero{margin-top:12px;background:linear-gradient(180deg,var(--panel-2),var(--panel));
  border:1px solid var(--line);border-radius:18px;padding:13px 14px 11px}
.lm-cap{font-family:var(--font-m);font-size:8.5px;letter-spacing:.17em;text-transform:uppercase;color:var(--faint)}
.lm-rate{display:flex;align-items:baseline;gap:6px;margin-top:2px}
.lm-rate .v{font-family:var(--font-d);font-weight:800;font-size:33px;letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:.95}
.lm-rate .u{font-family:var(--font-m);font-size:11px;color:var(--amber)}
.lm-rate .d{margin-left:auto;font-family:var(--font-m);font-size:9.5px;color:var(--ember);align-self:flex-end}
.lm-spark{width:100%;height:44px;display:block;margin-top:8px}
.lm-fuse{height:7px;border-radius:5px;background:#0c1117;border:1px solid var(--line);overflow:hidden;position:relative}
.lm-fuse>i{position:absolute;left:0;top:0;bottom:0;border-radius:5px;transition:width .5s}
.lm-fuse.mint>i{background:linear-gradient(90deg,#2fb98f,var(--mint))}
.lm-fuse.amber>i{background:linear-gradient(90deg,var(--mint),var(--amber));box-shadow:0 0 10px rgba(244,178,62,.4)}
.lm-fuse.ember>i{background:linear-gradient(90deg,var(--amber),var(--ember));box-shadow:0 0 12px rgba(255,87,75,.55)}
.lm-fuse.dead>i{background:#39424e;box-shadow:none}
.lm-agg{display:flex;justify-content:space-between;font-family:var(--font-m);font-size:9.5px;color:var(--dim);margin-top:7px}
.lm-agg b{color:var(--fg)}
/* segmented control */
.lm-seg{display:flex;gap:3px;background:#0c1117;border:1px solid var(--line);border-radius:11px;padding:3px;margin-top:14px}
.lm-seg button{flex:1;border:0;background:transparent;color:var(--dim);font-family:var(--font-t);font-weight:650;font-size:11.5px;padding:6px;border-radius:8px;cursor:pointer}
.lm-seg button.on{background:var(--panel-2);color:var(--fg);box-shadow:0 1px 0 rgba(255,255,255,.06) inset}
.lm-listcap{display:flex;justify-content:space-between;margin:13px 2px 7px}
.lm-listcap .l{font-family:var(--font-m);font-size:8.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint)}
/* run row */
.lm-run{display:flex;gap:9px;align-items:center;padding:9px;border-radius:13px;cursor:pointer;
  background:linear-gradient(180deg,rgba(255,255,255,.02),transparent);border:1px solid var(--line);margin-bottom:7px}
.lm-run:active{transform:scale(.985)}
.lm-run.crit{border-color:rgba(255,87,75,.4);background:linear-gradient(180deg,rgba(255,87,75,.07),transparent)}
.lm-run.dead{opacity:.5}
.lm-run .bd{width:30px;height:30px;border-radius:9px;flex:0 0 auto;display:grid;place-items:center;
  font-family:var(--font-m);font-size:12px;font-weight:700;background:#0c1117;border:1px solid var(--line-2);color:var(--dim)}
.lm-run .mid{flex:1;min-width:0}
.lm-run .idrow{display:flex;align-items:center;gap:7px}
.lm-run .id{font-family:var(--font-m);font-size:11px;color:var(--fg)}
.lm-run .rt{margin-left:auto;font-family:var(--font-m);font-size:9.5px;color:var(--amber)}
.lm-run .money{display:flex;justify-content:space-between;font-family:var(--font-m);font-size:8.5px;color:var(--dim);margin:5px 0 5px}
.lm-run .money b{color:var(--fg)}
.lm-pill{font-family:var(--font-m);font-size:7.5px;letter-spacing:.05em;text-transform:uppercase;padding:2px 6px;border-radius:999px;border:1px solid transparent;flex:0 0 auto}
.lm-pill.live{color:var(--mint);border-color:rgba(52,211,153,.35);background:rgba(52,211,153,.08)}
.lm-pill.near{color:var(--amber);border-color:rgba(244,178,62,.35);background:rgba(244,178,62,.08)}
.lm-pill.crit{color:var(--ember);border-color:rgba(255,87,75,.4);background:rgba(255,87,75,.1)}
.lm-pill.dead{color:var(--faint);border-color:var(--line-2)}
/* flagged-agents banner (runs) */
.lm-flag{display:flex;align-items:center;gap:9px;width:100%;text-align:left;margin-top:12px;padding:9px 11px;
  border-radius:13px;background:linear-gradient(180deg,rgba(255,87,75,.09),transparent);border:1px solid rgba(255,87,75,.35);cursor:pointer}
.lm-flag:active{transform:scale(.99)}
.lm-flag .fi{width:26px;height:26px;border-radius:8px;flex:0 0 auto;display:grid;place-items:center;background:rgba(255,87,75,.15);color:var(--ember)}
.lm-flag .fi svg{width:15px;height:15px}
.lm-flag .ft{flex:1;display:flex;flex-direction:column}
.lm-flag .ft b{font-family:var(--font-t);font-weight:700;font-size:12.5px;color:var(--fg)}
.lm-flag .ft span{font-family:var(--font-m);font-size:8.5px;color:var(--dim);margin-top:2px}
.lm-flag .fg{font-size:18px;color:var(--faint)}
/* device screen */
.lm-dvic{width:38px;height:38px;border-radius:11px;flex:0 0 auto;display:grid;place-items:center;background:#0c1117;border:1px solid var(--line-2);color:var(--dim)}
.lm-drow{display:flex;justify-content:space-between;align-items:center;font-family:var(--font-m);font-size:9.5px;color:var(--dim);border-top:1px solid var(--line);margin-top:11px;padding-top:9px}
.lm-drow b{color:var(--fg)}
.lm-mnote{font-family:var(--font-m);font-size:9.5px;color:var(--dim);line-height:1.5;margin-top:9px}
.lm-disc{width:100%;margin-top:16px;border:1px solid rgba(255,87,75,.4);background:rgba(255,87,75,.08);color:#ffb0a9;
  font-family:var(--font-t);font-weight:700;font-size:12px;border-radius:12px;padding:11px;cursor:pointer}
.lm-pairbtn{width:100%;margin-top:16px;border:1px solid var(--line-2);background:var(--panel);color:var(--fg);
  font-family:var(--font-t);font-weight:700;font-size:12px;border-radius:12px;padding:11px;cursor:pointer}
.lm-pairbtn:active{transform:scale(.99)}
/* agent detail */
.lm-chainrow{font-family:var(--font-m);font-size:11px;color:var(--fg);background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 12px}
.lm-act{flex:1;border:0;border-radius:12px;padding:11px;font-family:var(--font-t);font-weight:750;font-size:12.5px;cursor:pointer}
.lm-act.throttle{background:rgba(244,178,62,.14);border:1px solid rgba(244,178,62,.45);color:var(--amber)}
.lm-act.kill{background:linear-gradient(180deg,#ff6b60,#e23e33);color:#fff}
.lm-chev{margin-left:2px;align-self:center;font-size:16px;color:var(--faint);flex:0 0 auto}
/* tab bar */
.lm-tabs{display:flex;justify-content:space-around;padding:8px 14px 15px;border-top:1px solid var(--line);flex:0 0 auto}
.lm-tabs button{border:0;background:none;display:flex;flex-direction:column;align-items:center;gap:3px;
  font-family:var(--font-m);font-size:8px;letter-spacing:.05em;color:var(--faint);cursor:pointer}
.lm-tabs button.on{color:var(--accent)}
.lm-tabs svg{width:19px;height:19px}
/* detail */
.lm-back{align-self:flex-start;border:0;background:none;color:var(--accent);cursor:pointer;font:12px var(--font-t);padding:8px 2px 2px}
.lm-dnav{display:flex;align-items:center;gap:8px;padding-top:6px}
.lm-dnav .rid{font-family:var(--font-m);font-size:12px;color:var(--fg)}
.lm-gauge{margin-top:10px;background:linear-gradient(180deg,var(--panel-2),var(--panel));border:1px solid var(--line);border-radius:18px;padding:14px}
.lm-gauge .amt{font-family:var(--font-d);font-weight:800;font-size:34px;letter-spacing:-.03em;font-variant-numeric:tabular-nums;margin-top:2px}
.lm-gauge .of{font-family:var(--font-m);font-size:9.5px;color:var(--dim);margin:5px 0 9px}
.lm-gauge .of b{color:var(--fg)}
.lm-statgrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:11px}
.lm-stat{border:1px solid var(--line);border-radius:12px;padding:9px 10px;background:var(--panel)}
.lm-stat .k{font-family:var(--font-m);font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint)}
.lm-stat .v{font-family:var(--font-d);font-weight:750;font-size:17px;margin-top:3px}
/* slide to arm breaker */
.lm-killzone{padding:12px 14px 16px;flex:0 0 auto;border-top:1px solid var(--line)}
.lm-breaker{position:relative;height:52px;border-radius:15px;background:#0c1117;border:1px solid rgba(255,87,75,.45);overflow:hidden;touch-action:none;user-select:none;-webkit-user-select:none}
.lm-breaker .fill{position:absolute;left:0;top:0;bottom:0;width:44px;background:linear-gradient(90deg,rgba(255,87,75,.15),rgba(255,87,75,.4))}
.lm-breaker .knob{position:absolute;top:4px;left:4px;width:44px;height:42px;border-radius:11px;background:linear-gradient(180deg,#ff6b60,#e23e33);
  display:grid;place-items:center;box-shadow:0 6px 16px -6px rgba(255,87,75,.7);cursor:grab}
.lm-breaker .knob:active{cursor:grabbing}
.lm-breaker .knob svg{width:22px;height:22px}
.lm-breaker .lbl{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-family:var(--font-t);font-weight:700;font-size:13px;color:#ffb0a9;pointer-events:none;padding-left:30px}
.lm-breaker.armed{border-color:rgba(52,211,153,.6)}
.lm-breaker.armed .knob{background:linear-gradient(180deg,#46e3b4,#22a884)}
.lm-breaker.armed .lbl{color:var(--mint)}
.lm-khint{font-family:var(--font-m);font-size:8.5px;color:var(--faint);text-align:center;margin-top:9px}
/* live activity surfaces */
.lm-di-note{font-family:var(--font-m);font-size:8px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin:12px 0 6px}
.lm-di-compact{display:flex;align-items:center;justify-content:space-between;background:#000;border-radius:18px;padding:9px 14px}
.lm-di-compact .l{display:flex;align-items:center;gap:7px;font-family:var(--font-m);font-size:14px;font-weight:700;color:var(--fg)}
.lm-di-compact .ico{width:20px;height:20px;border-radius:6px;background:var(--amber);display:grid;place-items:center}
.lm-di-compact .ico svg{width:13px;height:13px}
.lm-di-exp{background:#0c1016;border:1px solid var(--line);border-radius:18px;padding:12px 14px}
.lm-di-exp .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px}
.lm-di-exp .rid{font-family:var(--font-m);font-size:10px;color:var(--dim)}
.lm-di-exp .big{font-family:var(--font-d);font-weight:800;font-size:22px}
.lm-killbtn{border:0;border-radius:11px;padding:8px 16px;font-family:var(--font-t);font-weight:750;font-size:12px;
  background:linear-gradient(180deg,#ff6b60,#e23e33);color:#fff;cursor:pointer}
.lm-lockcard{background:rgba(20,26,35,.85);border:1px solid var(--line);border-radius:16px;padding:12px 14px}
.lm-lockcard .h{display:flex;justify-content:space-between;font-family:var(--font-m);font-size:9.5px;color:var(--dim);margin-bottom:8px}
.lm-lockcard .app{display:flex;align-items:center;gap:6px;color:var(--fg)}
.lm-lockcard .app .b{width:14px;height:14px;border-radius:4px;background:var(--amber)}
/* pairing */
.lm-pair{flex:1;display:flex;flex-direction:column;align-items:center;text-align:center;padding:14px 20px}
.lm-reticle{position:relative;width:150px;height:150px;margin:14px 0 6px;border-radius:20px;background:#0c1016;border:1px solid var(--line)}
.lm-qr{position:absolute;inset:26px;border-radius:6px;background:#E9EEF5;padding:5px;color:#0B0F15}
.lm-qr svg{width:100%;height:100%;display:block}
.lm-pairsteps{width:100%;margin-top:13px;display:flex;flex-direction:column;gap:8px;text-align:left}
.lm-pairsteps div{display:flex;gap:9px;align-items:flex-start}
.lm-pairsteps b{font-family:var(--font-m);font-size:8.5px;font-weight:600;color:var(--iris);border:1px solid var(--line-2);
  border-radius:6px;width:17px;height:17px;display:grid;place-items:center;flex:0 0 auto}
.lm-pairsteps span{font-size:11px;color:var(--dim);line-height:1.45}
.lm-scan{position:absolute;left:14px;right:14px;height:2px;top:20px;background:var(--iris);box-shadow:0 0 14px var(--iris);animation:lmScan 2.4s ease-in-out infinite}
@keyframes lmScan{0%,100%{top:20px}50%{top:128px}}
.lm-corner{position:absolute;width:18px;height:18px;border:2px solid var(--iris)}
.lm-pair h2{font-family:var(--font-d);font-weight:750;font-size:17px;margin:12px 0 0}
.lm-pair p{color:var(--dim);font-size:12.5px;margin-top:6px;line-height:1.5}
.lm-seal{display:flex;gap:10px;text-align:left;margin-top:14px;border:1px solid var(--line);border-radius:14px;padding:11px 12px;background:var(--panel)}
.lm-seal svg{width:22px;height:22px;color:var(--mint);flex:0 0 auto;margin-top:1px}
.lm-seal .s{font-size:11px;color:var(--dim);line-height:1.5}
.lm-seal .s b{color:var(--fg)}
/* push / lock screen */
.lm-push{flex:1;display:flex;flex-direction:column;padding:16px 16px 12px;gap:10px}
.lm-locktime{text-align:center;margin:6px 0 8px}
.lm-locktime .t{font-family:var(--font-d);font-weight:700;font-size:44px;letter-spacing:-.02em;line-height:1}
.lm-locktime .d{font-size:12px;color:var(--dim);margin-top:2px}
.lm-banner{display:flex;gap:11px;background:rgba(20,26,35,.9);border:1px solid var(--line);border-radius:16px;padding:11px 13px;cursor:pointer}
.lm-banner:active{transform:scale(.99)}
.lm-banner .ic{width:26px;height:26px;border-radius:8px;flex:0 0 auto;display:grid;place-items:center}
.lm-banner .ic svg{width:16px;height:16px}
.lm-banner .ic.warn{background:rgba(244,178,62,.15);color:var(--amber)}
.lm-banner .ic.kill{background:rgba(255,87,75,.15);color:var(--ember)}
.lm-banner .bd{flex:1;min-width:0}
.lm-banner .tl{display:flex;justify-content:space-between;font-family:var(--font-m);font-size:9px;color:var(--dim)}
.lm-banner .msg{font-size:12px;color:var(--fg);margin-top:3px;line-height:1.4}
.lm-banner .msg .id{font-family:var(--font-m);color:var(--amber)}
.lm-banner .msg .idk{font-family:var(--font-m);color:var(--ember)}
/* toast */
.lm-toast{position:absolute;left:14px;right:14px;bottom:70px;background:#10161F;border:1px solid var(--line-2);
  border-radius:12px;padding:9px 12px;font-family:var(--font-m);font-size:9px;color:var(--mint);
  opacity:0;transform:translateY(8px);transition:opacity .3s,transform .3s;pointer-events:none;z-index:30;text-align:center}
.lm-toast.on{opacity:1;transform:none}
/* ---- Apple Watch frame ---- */
.lm-watchcol{display:flex;flex-direction:column;align-items:center;gap:10px;flex:0 0 auto}
.lm-watch{position:relative;width:158px;flex:0 0 auto}
.lm-wscr{aspect-ratio:198/242;border-radius:38px;border:1px solid var(--line-2);overflow:hidden;background:#000;
  position:relative;box-shadow:0 0 0 5px #10151d,0 0 0 6px rgba(255,255,255,.09),0 20px 44px -18px rgba(0,0,0,.8)}
.lm-crown{position:absolute;right:-4px;top:30%;width:4px;height:26px;border-radius:3px;background:#2a3547}
.lm-wview{position:absolute;inset:12px 12px 10px;display:none;flex-direction:column;font-family:var(--font-t)}
.lm-wview.on{display:flex;animation:lmSlide .3s ease}
.lm-wtime{font-family:var(--font-m);font-size:8px;color:var(--faint);text-align:right}
.lm-wbig{font-family:var(--font-d);font-weight:800;font-size:30px;letter-spacing:-.03em;font-variant-numeric:tabular-nums;line-height:1}
.lm-wbig .cu{font-size:11px;color:var(--dim)}
.lm-wsub{font-family:var(--font-m);font-size:7.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim)}
.lm-wrow{display:flex;justify-content:space-between;align-items:center;font-family:var(--font-m);font-size:8px;color:var(--dim);padding:3px 0}
.lm-wrow b{color:var(--fg);font-size:10px}
.lm-wrun{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.06);font-family:var(--font-m);font-size:8.5px}
.lm-wrun .id{color:var(--fg)}
.lm-wbtn{margin-top:auto;position:relative;border-radius:13px;border:1px solid rgba(255,87,75,.5);
  background:rgba(255,87,75,.14);color:#ffb0a9;font-weight:750;font-size:11px;font-family:var(--font-t);
  padding:10px 6px;width:100%;cursor:pointer;overflow:hidden;user-select:none;-webkit-user-select:none;touch-action:none}
.lm-wbtn>i{position:absolute;left:0;top:0;bottom:0;width:0;background:rgba(255,87,75,.4)}
.lm-wbtn>span{position:relative}
.lm-wbtn.armed{background:linear-gradient(180deg,#ff6b60,#e23e33);color:#fff;border-color:transparent}
.lm-wbtn.done{background:rgba(52,211,153,.14);border-color:rgba(52,211,153,.5);color:var(--mint)}
.lm-wface{align-items:center;justify-content:center;text-align:center;gap:2px}
.lm-wswitch{display:flex;gap:5px;flex-wrap:wrap;justify-content:center}
.lm-wswitch button{border:1px solid var(--line-2);background:var(--panel-2);color:var(--dim);
  font-family:var(--font-m);font-size:9px;border-radius:8px;padding:5px 9px;cursor:pointer}
.lm-wswitch button.on{color:var(--fg);border-color:color-mix(in srgb,var(--accent) 55%,var(--line-2))}
.lm-note{font-family:var(--font-m);font-size:8.5px;color:var(--faint);text-align:center}
/* ---- Sphere: real screenshot frames ---- */
.lm-shot{position:absolute;inset:5px;border-radius:41px;overflow:hidden;background:#070A0F}
.lm-shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .5s}
.lm-shot img.on{opacity:1}
.lm-wshot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .4s}
.lm-wshot img.on{opacity:1}
@media (prefers-reduced-motion: reduce){
  .lm-view.on,.lm-wview.on{animation:none}.lm-scan{animation:none}
  .lm-fuse>i,.lm-shot img,.lm-wshot img{transition:none}
}
`;
let cssDone=false;
function ensureCss(){ if(cssDone) return; cssDone=true;
  const st=document.createElement("style");st.textContent=CSS;document.head.appendChild(st); }

/* wire a column of .as-step cards to drive a mock (click -> fn(i), highlight active) */
function wireSteps(stepsEl,fn){
  if(!stepsEl) return;
  const steps=[...stepsEl.querySelectorAll(".as-step")];
  const act=i=>steps.forEach((s,j)=>s.classList.toggle("on",j===i));
  steps.forEach((s,i)=>{
    s.setAttribute("role","button");s.setAttribute("tabindex","0");
    s.addEventListener("click",()=>{act(i);fn(i);});
    s.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();act(i);fn(i);}});
  });
  act(0);
}
/* status-bar signal + battery svg (shared) */
const SB=`<span class="r"><svg width="16" height="10" viewBox="0 0 17 11" fill="currentColor"><rect x="0" y="7" width="3" height="4" rx="1"/><rect x="4.5" y="5" width="3" height="6" rx="1"/><rect x="9" y="2.5" width="3" height="8.5" rx="1"/><rect x="13.5" y="0" width="3" height="11" rx="1"/></svg><svg width="22" height="11" viewBox="0 0 24 12" fill="none"><rect x="1" y="1.5" width="19" height="9" rx="2.5" stroke="currentColor" opacity=".5"/><rect x="2.5" y="3" width="14" height="6" rx="1.2" fill="currentColor"/></svg></span>`;

/* A code that reads as a QR at a glance: three finder patterns, the timing
   rows, and deterministic modules in between. Decoration for the mock, so it
   carries no payload and is not scannable. */
function qrPattern(n){
  n=n||25;const cells=[];
  const finder=(x,y)=>{
    for(const[cx,cy]of [[3,3],[n-4,3],[3,n-4]]){
      const d=Math.max(Math.abs(x-cx),Math.abs(y-cy));
      if(d<=4) return d===4?false:d!==2;
    }
    return null;
  };
  for(let y=0;y<n;y++)for(let x=0;x<n;x++){
    const f=finder(x,y);let on;
    if(f!==null) on=f;
    else if(x===6||y===6) on=(x+y)%2===0;
    else on=((((x*73856093)^(y*19349663)^((x*y)*83492791))>>>7)&3)>1;
    if(on)cells.push(`<rect x="${x}" y="${y}" width="1" height="1"/>`);
  }
  return `<svg viewBox="0 0 ${n} ${n}" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges" fill="currentColor" aria-hidden="true">${cells.join("")}</svg>`;
}

/* draw a sparkline into a canvas, value 0..1 array, color */
function spark(cv,vals,col,fillA){
  const ctx=cv.getContext("2d"), dpr=Math.min(2,devicePixelRatio||1);
  const w=cv.clientWidth||260,h=cv.clientHeight||44;
  cv.width=w*dpr;cv.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,w,h);
  ctx.beginPath();
  vals.forEach((v,i)=>{const x=w*i/(vals.length-1),y=h-3-(h-6)*v;i?ctx.lineTo(x,y):ctx.moveTo(x,y);});
  ctx.strokeStyle=col;ctx.lineWidth=1.8;ctx.stroke();
  ctx.lineTo(w,h);ctx.lineTo(0,h);ctx.closePath();
  const g=ctx.createLinearGradient(0,0,0,h);g.addColorStop(0,col+"44");g.addColorStop(1,col+"00");
  ctx.fillStyle=g;ctx.fill();
}

/* slide-to-arm: drag the knob to the right end to fire cb once */
function slideToArm(track,onArm){
  const knob=$(track,".knob"), fill=$(track,".fill"), lbl=$(track,".lbl");
  let drag=false,armed=false;
  function reset(){ if(armed) return; knob.style.left="4px"; fill.style.width="44px"; }
  function pos(x){
    const r=track.getBoundingClientRect(), max=r.width-52;
    let px=Math.max(4,Math.min(max, x-r.left-24));
    knob.style.left=px+"px"; fill.style.width=(px+44)+"px";
    return px>=max-2;
  }
  knob.addEventListener("pointerdown",e=>{if(armed)return;drag=true;knob.setPointerCapture(e.pointerId);});
  track.addEventListener("pointermove",e=>{ if(!drag||armed)return;
    if(pos(e.clientX)){ armed=true;drag=false;track.classList.add("armed");
      lbl.textContent="Killed · breaker open"; onArm(); } });
  track.addEventListener("pointerup",()=>{drag=false;reset();});
  track.addEventListener("pointercancel",()=>{drag=false;reset();});
  return {isArmed:()=>armed, arm:()=>{if(armed)return;armed=true;const r=track.getBoundingClientRect();
    knob.style.left=(r.width-48)+"px";fill.style.width="100%";track.classList.add("armed");lbl.textContent="Killed · breaker open";}};
}
/* hold-to-fire (watch) */
function hold(btn,ms,cb){
  const bar=$(btn,"i");let t0=null,tm=null;
  function stop(f){clearInterval(tm);tm=null;t0=null;if(!f)bar.style.width="0";}
  btn.addEventListener("pointerdown",e=>{if(btn.classList.contains("done"))return;btn.setPointerCapture(e.pointerId);t0=performance.now();
    tm=setInterval(()=>{const p=Math.min(1,(performance.now()-t0)/ms);bar.style.width=(p*100)+"%";if(p>=1){stop(1);cb();}},30);});
  btn.addEventListener("pointerup",()=>stop(0));btn.addEventListener("pointercancel",()=>stop(0));
}

/* =================================================================
   POCKET: full iPhone (5 screens) + Apple Watch (5 screens)
   ================================================================= */
function pocket(root,stepsEl){
  ensureCss();
  const S={
    runs:[
      {id:"7f3a2b",badge:"O",model:"opus-4-8",step:41,burn:1.90,spent:26.10,cap:25,st:"crit"},
      {id:"b12e90",badge:"S",model:"sonnet",step:18,burn:0.31,spent:8.40,cap:10,st:"near"},
      {id:"4c07af",badge:"H",model:"haiku",step:6,burn:0.06,spent:1.20,cap:8,st:"live"}
    ],
    filter:"active", sel:0, sparkV:Array.from({length:32},(_,i)=>0.4+0.28*Math.sin(i*0.5)+0.2*Math.sin(i*0.17)),
    /* Budgets ladder: org -> team -> agent. The tree is the source of truth;
       team and org spend are summed from it, so any drill-in reconciles. */
    bscope:"agent", bsel:null,
    btree:{
      org:{name:"acme", cap:43},
      teams:[
        {name:"support",  cap:20, agents:[
          {name:"support/tier1",      cap:10, spent:8.40},
          {name:"support/tier2",      cap:10, spent:4.20}
        ]},
        {name:"research", cap:15, agents:[
          {name:"research/analyst",   cap:8,  spent:6.10, flagged:"excessive_agency"},
          {name:"research/summariser",cap:5,  spent:2.30}
        ]},
        {name:"batch",    cap:5,  agents:[
          {name:"batch/crawler",      cap:5,  spent:5.00, flagged:"runaway_agent"}
        ]}
      ]
    },
    /* Behaviour: agents flagged by detectors, worst first. sev maps to the
       existing crit/near/live pill classes (critical / elevated / watch). */
    asort:"risk", asel:0,
    agents:[
      {id:"batch/crawler",   det:"runaway_agent",   sev:"crit", why:"41 steps in 3 min, no human in the loop, 4.5x its usual rate", chain:"support → analyst → crawler", blast:12, seen:"now"},
      {id:"research/analyst",det:"excessive_agency", sev:"near", why:"reached 3 tools it had never called before this run",         chain:"support → analyst",           blast:7,  seen:"2m"},
      {id:"svc/legacy-key",  det:"orphaned_nhi",     sev:"near", why:"non-human identity, no owner, unused 41 days",                 chain:"—",                           blast:3,  seen:"9m"},
      {id:"tool/unknown",    det:"shadow_ai",        sev:"live", why:"undeclared model endpoint first seen on the bus",              chain:"—",                           blast:1,  seen:"14m"}
    ]
  };
  const T=(s)=>{ // tab icons
    return {runs:'<path d="M4 13h4l2 5 4-12 2 7h4"/>',bud:'<path d="M12 20v-6M12 10V4M5 20v-9M5 7V4M19 20v-3M19 13V4"/><circle cx="12" cy="12" r="2"/><circle cx="5" cy="9" r="2"/><circle cx="19" cy="15" r="2"/>',alr:'<path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>',dev:'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>'}[s];
  };
  /* One tab bar for every screen that carries one. `on` is the tab that owns
     the screen, so a drill-in (a run, an agent, a budget scope) still shows
     its parent tab lit rather than nothing. */
  const TABBAR=on=>'<div class="lm-tabs" data-tabs>'+
    [["runs","Runs","runs"],["budgets","Budgets","bud"],["alerts","Alerts","alr"],["device","Device","dev"]]
      .map(([k,label,ico])=>`<button${on===k?' class="on"':""} data-tab="${k}">`+
        `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${T(ico)}</svg>${label}</button>`)
      .join("")+"</div>";
  root.classList.add("lm-wrap");
  root.innerHTML=
   `<figure class="lm-phone" style="margin:0"><span class="lm-island"></span>
     <div class="lm-scr">
       <div class="lm-sb"><span data-clk>9:41</span>${SB}</div>
       <div class="lm-body">
         <!-- RUNS -->
         <div class="lm-view on" data-v="runs">
           <div class="lm-scroll">
             <div class="lm-h1">Runs</div>
             <span class="lm-chip"><span class="k"></span>acme · 3 gateways · live</span>
             <div class="lm-hero">
               <div class="lm-cap">Fleet burn rate</div>
               <div class="lm-rate"><span class="v" data-fb>1.90</span><span class="u">$/min</span><span class="d" data-fd>+4.5x baseline</span></div>
               <canvas class="lm-spark" data-spark></canvas>
               <div class="lm-fuse amber" data-ffuse><i style="width:73%"></i></div>
               <div class="lm-agg"><span>spent today <b data-ftot>$18.30</b></span><span>caps <b>$43.00</b></span></div>
             </div>
             <button class="lm-flag" data-goto-agents>
               <span class="fi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 21V4h11l-1.5 3.5L15 11H4"/></svg></span>
               <span class="ft"><b>3 agents flagged</b><span>behaviour · runaway, excessive agency</span></span>
               <span class="fg">›</span>
             </button>
             <div class="lm-seg" data-seg>
               <button class="on" data-f="active">Active</button><button data-f="all">All</button><button data-f="killed">Killed</button>
             </div>
             <div class="lm-listcap"><span class="l" data-lcount>3 active</span><span class="l" style="color:var(--iris)">sort · burn</span></div>
             <div data-runs></div>
           </div>
           ${TABBAR("runs")}
         </div>
         <!-- DETAIL -->
         <div class="lm-view" data-v="detail">
           <div class="lm-scroll">
             <button class="lm-back" data-back>‹ Runs</button>
             <div class="lm-dnav"><span class="rid" data-did>run 7f3a2b</span><span class="lm-pill crit" data-dpill>over cap</span></div>
             <div class="lm-gauge">
               <div class="lm-cap">Spent</div>
               <div class="amt" data-damt style="color:var(--ember)">$26.10</div>
               <div class="of" data-dof>of <b>$25.00</b> cap · 104% · burning $1.90/min</div>
               <div class="lm-fuse ember" data-dfuse style="height:9px"><i style="width:100%"></i></div>
             </div>
             <div class="lm-statgrid">
               <div class="lm-stat"><div class="k">Steps</div><div class="v" data-dstep>41</div></div>
               <div class="lm-stat"><div class="k">Calls</div><div class="v">312</div></div>
               <div class="lm-stat"><div class="k">Model</div><div class="v" data-dmodel style="font-size:12px;font-family:var(--font-m)">opus-4-8</div></div>
             </div>
           </div>
           <div class="lm-killzone">
             <div class="lm-breaker" data-breaker>
               <div class="fill"></div>
               <div class="knob"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4"><path d="M18.4 5.6a9 9 0 1 1-12.8 0"/><path d="M12 2v9"/></svg></div>
               <div class="lbl">Slide to arm kill</div>
             </div>
             <div class="lm-khint">Kill is signed by the Secure Enclave · Face ID</div>
           </div>
           ${TABBAR("runs")}
         </div>
         <!-- LIVE ACTIVITY -->
         <div class="lm-view" data-v="island">
           <div class="lm-scroll">
             <div class="lm-h1">Always in view</div>
             <div class="lm-di-note">Dynamic Island · compact</div>
             <div class="lm-di-compact">
               <span class="l"><span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="#0a0e13" stroke-width="2.6"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg></span><span data-diburn>1.90</span><span style="font-family:var(--font-m);font-size:10px;color:var(--dim)">$/m</span></span>
               <span style="font-family:var(--font-m);font-size:10px;color:var(--ember)">104%</span>
             </div>
             <div class="lm-di-note">Long-press · expanded</div>
             <div class="lm-di-exp">
               <div class="top"><span class="rid">run 7f3a2b · opus-4-8</span><span class="lm-pill crit">over cap</span></div>
               <div style="display:flex;align-items:flex-end;justify-content:space-between">
                 <div><span class="big">$26.10</span> <span style="font-family:var(--font-m);font-size:11px;color:var(--dim)">of $25.00</span></div>
                 <button class="lm-killbtn" data-dikill>Kill</button>
               </div>
               <div class="lm-fuse ember" style="height:9px;margin-top:11px"><i style="width:100%"></i></div>
             </div>
             <div class="lm-di-note">Lock Screen · Live Activity</div>
             <div class="lm-lockcard">
               <div class="h"><span class="app"><span class="b"></span>TokenFuse</span><span>now</span></div>
               <div style="display:flex;justify-content:space-between;align-items:baseline">
                 <span class="big" style="font-family:var(--font-d);font-weight:800;font-size:20px">$26.10 <span style="font-size:12px;color:var(--dim);font-family:var(--font-m)">/ $25.00</span></span>
                 <span style="font-family:var(--font-m);font-size:11px;color:var(--ember)">$1.90/m</span>
               </div>
               <div class="lm-fuse ember" style="height:9px;margin-top:9px"><i style="width:100%"></i></div>
             </div>
           </div>
           ${TABBAR("alerts")}
         </div>
         <!-- PAIRING -->
         <div class="lm-view" data-v="pair">
           <div class="lm-pair">
             <button class="lm-back" data-back-device>‹ Device</button>
             <div class="lm-cap" style="color:var(--iris)">Pair this iPhone</div>
             <div class="lm-reticle">
               <div class="lm-qr">${qrPattern(25)}</div><div class="lm-scan"></div>
               <div class="lm-corner" style="top:8px;left:8px;border-right:0;border-bottom:0"></div>
               <div class="lm-corner" style="top:8px;right:8px;border-left:0;border-bottom:0"></div>
               <div class="lm-corner" style="bottom:8px;left:8px;border-right:0;border-top:0"></div>
               <div class="lm-corner" style="bottom:8px;right:8px;border-left:0;border-top:0"></div>
             </div>
             <h2>Scan the code on your console</h2>
             <p>A one-time code links this device to your org. It expires in <b data-pairttl style="font-family:var(--font-m);color:var(--fg)">9:58</b>.</p>
             <div class="lm-seal">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>
               <div class="s"><b>Keys never leave this iPhone.</b> A signing key is generated in the Secure Enclave, so a stolen token alone cannot stop your agents.</div>
             </div>
             <div class="lm-pairsteps">
               <div><b>1</b><span>Your console issues the code. It is single use and expires.</span></div>
               <div><b>2</b><span>Scanning it enrols this phone and mints the on-device key.</span></div>
               <div><b>3</b><span>From then on the phone reaches your box over the tunnel, never the open internet.</span></div>
             </div>
           </div>
         </div>
         <!-- ALERTS / PUSH -->
         <div class="lm-view" data-v="push">
           <div class="lm-push">
             <div class="lm-locktime"><div class="t" data-clk2>9:41</div><div class="d">Thursday, 3 July</div></div>
             <div class="lm-banner" data-goto="detail">
               <span class="ic warn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M13 2 4 14h6l-1 8 9-12h-6z"/></svg></span>
               <div class="bd"><div class="tl"><span>TokenFuse</span><span>now</span></div>
                 <div class="msg">Run <span class="id">b12e90</span> hit 90% of its $10.00 cap, burning $0.31/min.</div></div>
             </div>
             <div class="lm-banner" data-goto="detail">
               <span class="ic kill"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18.4 5.6a9 9 0 1 1-12.8 0"/><path d="M12 2v9"/></svg></span>
               <div class="bd"><div class="tl"><span>TokenFuse</span><span>2m ago</span></div>
                 <div class="msg">Killed <span class="idk">7f3a2b</span> across 3 gateways. Signed on this iPhone.</div></div>
             </div>
             <div class="lm-note" style="margin-top:4px">Tap a budget alert → Face ID → killed, without opening the app.</div>
           </div>
           ${TABBAR("alerts")}
         </div>
         <!-- BUDGET detail: drill into a scope -->
         <div class="lm-view" data-v="budgetdet">
           <div class="lm-scroll">
             <button class="lm-back" data-back-budgets>‹ Budgets</button>
             <div class="lm-dnav"><span class="rid" data-bdid>name</span><span class="lm-pill crit" data-bdpill>scope</span></div>
             <div class="lm-gauge" style="margin-top:10px">
               <div class="lm-cap" data-bdcap>spend</div>
               <div class="amt" data-bdamt style="font-size:30px">$0</div>
               <div class="of" data-bdof>of cap</div>
               <div class="lm-fuse amber" data-bdfuse><i style="width:0%"></i></div>
             </div>
             <div class="lm-cap" style="margin:15px 0 7px" data-bdlabel>Breakdown</div>
             <div data-bdkids></div>
           </div>
           ${TABBAR("budgets")}
         </div>
         <!-- BUDGETS -->
         <div class="lm-view" data-v="budgets">
           <div class="lm-scroll">
             <div class="lm-h1">Budgets</div>
             <span class="lm-chip"><span class="k"></span>caps above the run · org · team · agent</span>
             <div class="lm-seg" data-bseg>
               <button data-b="org">Org</button><button data-b="team">Teams</button><button class="on" data-b="agent">Agents</button>
             </div>
             <div class="lm-listcap"><span class="l" data-bcount>3 agents</span><span class="l" style="color:var(--iris)">80% warn · 95% alert</span></div>
             <div data-budgets></div>
           </div>
           ${TABBAR("budgets")}
         </div>
         <!-- DEVICE -->
         <div class="lm-view" data-v="device">
           <div class="lm-scroll">
             <div class="lm-h1">Device</div>
             <span class="lm-chip"><span class="k"></span>this iPhone · paired · signing key on-device</span>
             <div class="lm-gauge" style="margin-top:12px">
               <div class="lm-cap">Paired device</div>
               <div style="display:flex;align-items:center;gap:10px;margin-top:8px">
                 <div class="lm-dvic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/></svg></div>
                 <div><div style="font-family:var(--font-t);font-weight:700;font-size:14px;color:var(--fg)">Yurii · iPhone</div><div style="font-family:var(--font-m);font-size:9.5px;color:var(--dim);margin-top:2px">paired 3 Jul · Secure Enclave key <b style="color:var(--fg)">a91c…4e2</b></div></div>
               </div>
               <div class="lm-drow"><span>Last signed action</span><b>killed 7f3a2b · 2m ago</b></div>
             </div>
             <div class="lm-cap" style="margin:16px 0 7px">Remote access over the tunnel</div>
             <div class="lm-seg" data-mseg>
               <button class="on" data-m="default">Default</button><button data-m="strict">Strict</button>
             </div>
             <div class="lm-mnote" data-mnote>Phone stays paired; you toggle the tunnel off when done, and idle peers are dropped. Reconnect needs no new code.</div>
             <div class="lm-seal" style="margin-top:14px">
               <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>
               <div class="s"><b>Keys never leave this iPhone.</b> A stolen session cannot act: every destructive action is re-signed here with Face ID.</div>
             </div>
             <button class="lm-pairbtn" data-goto-pair>Pair another device</button>
             <button class="lm-disc" data-disc style="margin-top:9px">Disconnect this device</button>
           </div>
           ${TABBAR("device")}
         </div>
         <!-- AGENTS (behaviour) -->
         <div class="lm-view" data-v="agents">
           <div class="lm-scroll">
             <button class="lm-back" data-back-runs>‹ Runs</button>
             <div class="lm-h1">Agents</div>
             <span class="lm-chip"><span class="k" style="background:var(--ember);box-shadow:0 0 8px var(--ember)"></span>behaviour · idryx detections · shares the bus</span>
             <div class="lm-seg" data-asort>
               <button class="on" data-s="risk">By risk</button><button data-s="recent">Recent</button>
             </div>
             <div class="lm-listcap"><span class="l" data-acount>4 flagged</span><span class="l" style="color:var(--iris)">worst first</span></div>
             <div data-agents></div>
           </div>
           ${TABBAR("runs")}
         </div>
         <!-- AGENT detail: why it was flagged -->
         <div class="lm-view" data-v="agentdet">
           <div class="lm-scroll">
             <button class="lm-back" data-back-agents>‹ Agents</button>
             <div class="lm-dnav"><span class="rid" data-adid>agent</span><span class="lm-pill crit" data-adpill>detector</span></div>
             <div class="lm-gauge" style="margin-top:10px">
               <div class="lm-cap" data-addet>runaway_agent</div>
               <div style="font-family:var(--font-t);font-size:13px;color:var(--fg);line-height:1.5;margin-top:7px" data-adwhy>why</div>
             </div>
             <div class="lm-statgrid">
               <div class="lm-stat"><div class="k">Chain</div><div class="v" data-adchain style="font-size:11px;font-family:var(--font-m)">3 deep</div></div>
               <div class="lm-stat"><div class="k">Blast</div><div class="v" data-adblast>12</div></div>
               <div class="lm-stat"><div class="k">Seen</div><div class="v" data-adseen style="font-size:13px">now</div></div>
             </div>
             <div class="lm-cap" style="margin:15px 0 7px">Delegation chain</div>
             <div class="lm-chainrow" data-adchainrow>support → analyst → crawler</div>
           </div>
           <div class="lm-killzone">
             <div style="display:flex;gap:8px">
               <button class="lm-act throttle" data-throttle>Throttle</button>
               <button class="lm-act kill" data-agkill>Kill agent</button>
             </div>
             <div class="lm-khint">A kill is signed by the Secure Enclave · Face ID. Nothing here is armed by a tap alone.</div>
           </div>
           ${TABBAR("runs")}
         </div>
         <div class="lm-toast" data-toast></div>
       </div>
     </div>
   </figure>
   <div class="lm-watchcol">
     <figure class="lm-watch" style="margin:0"><span class="lm-crown"></span>
       <div class="lm-wscr">
         <div class="lm-wview lm-wface on" data-w="face">
           <div class="lm-wtime" data-wclk>9:41</div>
           <div style="margin:auto 0"><div class="lm-wsub">fleet burn</div>
             <div class="lm-wbig" data-wface>1.90<span class="cu"> $/m</span></div>
             <div class="lm-wsub" style="color:var(--ember);margin-top:3px">1 over cap</div></div>
         </div>
         <div class="lm-wview" data-w="fleet">
           <div class="lm-wsub">Fleet</div>
           <div class="lm-wbig" data-wfleet style="margin-top:6px">1.90<span class="cu"> $/m</span></div>
           <div class="lm-wrow"><span>runs</span><b>3 live</b></div>
           <div class="lm-wrow"><span>spent</span><b>$35.70</b></div>
           <div class="lm-wrow"><span>over cap</span><b style="color:var(--ember)">1</b></div>
         </div>
         <div class="lm-wview" data-w="runs">
           <div class="lm-wsub">Runs</div>
           <div data-wruns style="margin-top:5px"></div>
         </div>
         <div class="lm-wview" data-w="kill">
           <div class="lm-wsub">Kill hottest</div>
           <div class="lm-wbig" style="font-size:15px;margin-top:6px">7f3a2b</div>
           <div class="lm-wrow"><span>opus-4-8</span><b style="color:var(--ember)">$1.90/m</b></div>
           <button class="lm-wbtn" data-wkill><i></i><span>hold to kill</span></button>
         </div>
         <div class="lm-wview lm-wface" data-w="killed">
           <div style="margin:auto 0;text-align:center">
             <div style="width:40px;height:40px;border-radius:50%;border:2px solid var(--mint);margin:0 auto 8px;display:grid;place-items:center;color:var(--mint)">✓</div>
             <div class="lm-wsub" style="color:var(--mint)">killed · breaker open</div>
             <div class="lm-wsub" style="margin-top:4px">signed on wrist</div></div>
         </div>
       </div>
     </figure>
     <div class="lm-wswitch" data-wswitch>
       <button class="on" data-ws="face">Face</button><button data-ws="fleet">Fleet</button><button data-ws="runs">Runs</button><button data-ws="kill">Kill</button><button data-ws="killed">Killed</button>
     </div>
     <div class="lm-note">shares state with the phone</div>
   </div>`;

  const el={
    fb:$(root,"[data-fb]"),fd:$(root,"[data-fd]"),ftot:$(root,"[data-ftot]"),ffuse:$(root,"[data-ffuse]"),
    runs:$(root,"[data-runs]"),lcount:$(root,"[data-lcount]"),spark:$(root,"[data-spark]"),
    did:$(root,"[data-did]"),dpill:$(root,"[data-dpill]"),damt:$(root,"[data-damt]"),dof:$(root,"[data-dof]"),
    dfuse:$(root,"[data-dfuse]"),dstep:$(root,"[data-dstep]"),dmodel:$(root,"[data-dmodel]"),
    breaker:$(root,"[data-breaker]"),toast:$(root,"[data-toast]"),diburn:$(root,"[data-diburn]"),
    wface:$(root,"[data-wface]"),wfleet:$(root,"[data-wfleet]"),wruns:$(root,"[data-wruns]"),
    wkill:$(root,"[data-wkill]"),clk:$$(root,"[data-clk],[data-clk2],[data-wclk]")
  };
  el.clk.forEach(c=>c.textContent=clock());
  let view="runs", arm=null;

  function show(v){ view=v;
    $$(root,".lm-view").forEach(x=>x.classList.toggle("on",x.dataset.v===v));
    const tabFor={runs:"runs",detail:"runs",agents:"runs",agentdet:"runs",
                  budgets:"budgets",budgetdet:"budgets",
                  push:"alerts",island:"alerts",device:"device"}[v]||"";
    $$(root,"[data-tab]").forEach(b=>b.classList.toggle("on",b.dataset.tab===tabFor));
  }
  function toast(m){el.toast.textContent=m;el.toast.classList.add("on");setTimeout(()=>el.toast.classList.remove("on"),2600);}
  function pill(r){return r.st==="dead"?["dead","killed"]:r.st==="crit"?["crit","over cap"]:r.st==="near"?["near","near cap"]:["live","live"];}
  function fcls(r){return r.st==="dead"?"dead":r.spent/r.cap>.98?"ember":r.spent/r.cap>.7?"amber":"mint";}
  function rtcol(r){return r.st==="dead"?"var(--faint)":r.st==="crit"?"var(--ember)":r.st==="live"?"var(--mint)":"var(--amber)";}

  function renderRuns(){
    const list=S.runs.filter(r=>S.filter==="all"?1:S.filter==="killed"?r.st==="dead":r.st!=="dead");
    el.lcount.textContent=list.length+" "+S.filter;
    el.runs.innerHTML=list.map(r=>{const i=S.runs.indexOf(r);const[pc,pt]=pill(r);
      return `<div class="lm-run ${r.st==="crit"?"crit":""} ${r.st==="dead"?"dead":""}" data-i="${i}">
        <div class="bd" style="${r.st==="crit"?"color:var(--ember);border-color:rgba(255,87,75,.4)":""}">${r.badge}</div>
        <div class="mid">
          <div class="idrow"><span class="id">${r.id}</span><span class="lm-pill ${pc}">${pt}</span><span class="rt" style="color:${rtcol(r)}">$${f2(r.st==="dead"?0:r.burn)}/m</span></div>
          <div class="money"><span>${r.model} · step ${r.step}</span><span><b style="color:${r.st==="crit"?"var(--ember)":"var(--fg)"}">$${f2(r.spent)}</b> / $${r.cap}</span></div>
          <div class="lm-fuse ${fcls(r)}"><i style="width:${Math.min(104,r.spent/r.cap*100)}%"></i></div>
        </div></div>`;}).join("")||`<div class="lm-note" style="padding:20px">no runs in this filter</div>`;
  }
  function renderWRuns(){
    el.wruns.innerHTML=S.runs.map(r=>`<div class="lm-wrun"><span class="id">${r.id}</span><b style="color:${rtcol(r)}">$${f2(r.st==="dead"?0:r.burn)}</b></div>`).join("");
  }
  function renderDetail(){
    const r=S.runs[S.sel];const over=r.spent/r.cap;
    el.did.textContent="run "+r.id;
    const[pc,pt]=pill(r);el.dpill.className="lm-pill "+pc;el.dpill.textContent=pt;
    el.damt.textContent="$"+f2(r.spent);el.damt.style.color=over>.98?"var(--ember)":"var(--fg)";
    el.dof.innerHTML="of <b>$"+r.cap.toFixed(2)+"</b> cap · "+Math.round(over*100)+"% · "+(r.st==="dead"?"killed":"burning $"+f2(r.burn)+"/min");
    el.dfuse.className="lm-fuse "+fcls(r);$(el.dfuse,"i").style.width=Math.min(104,over*100)+"%";
    el.dstep.textContent=r.step;el.dmodel.textContent=r.model;
    /* rebuild the breaker fresh so the slider resets per run (unless already dead) */
    if(r.st!=="dead"){
      el.breaker.classList.remove("armed");$(el.breaker,".knob").style.left="4px";$(el.breaker,".fill").style.width="44px";$(el.breaker,".lbl").textContent="Slide to arm kill";
      arm=slideToArm(el.breaker,()=>killRun(S.sel,"phone"));
    }else{
      el.breaker.classList.add("armed");$(el.breaker,".fill").style.width="100%";$(el.breaker,".lbl").textContent="Killed · breaker open";
      const k=$(el.breaker,".knob");k.style.left="calc(100% - 48px)";
    }
  }
  const teamSpent=t=>t.agents.reduce((a,x)=>a+x.spent,0);
  const orgSpent=()=>S.btree.teams.reduce((a,t)=>a+teamSpent(t),0);
  const allAgents=()=>S.btree.teams.flatMap(t=>t.agents.map(a=>({...a,team:t.name})));
  function budgetRow(name,spent,cap,sub,tag,i,flagged){
    const over=cap?spent/cap:0, cls=over>=.95?"ember":over>=.8?"amber":"mint";
    const pill=over>=1?["crit","over cap"]:over>=.95?["crit","95%"]:over>=.8?["near","80%"]:["live","ok"];
    return `<div class="lm-run ${over>=1?"crit":""}" data-bi="${i}">
      <div class="bd">${tag}</div>
      <div class="mid">
        <div class="idrow"><span class="id">${name}</span><span class="lm-pill ${pill[0]}">${pill[1]}</span><span class="rt" style="color:var(--dim)">${Math.round(over*100)}%</span></div>
        <div class="money"><span>${sub}${flagged?" · flagged":""}</span><span><b style="color:${over>=1?'var(--ember)':'var(--fg)'}">$${f2(spent)}</b> / $${cap.toFixed(2)}</span></div>
        <div class="lm-fuse ${cls}"><i style="width:${Math.min(104,over*100)}%"></i></div>
      </div>
      <span class="lm-chev">›</span></div>`;
  }
  function renderBudgets(){
    let rows;
    if(S.bscope==="org"){
      rows=budgetRow(S.btree.org.name,orgSpent(),S.btree.org.cap,S.btree.teams.length+" teams","O",0);
      $(root,"[data-bcount]").textContent="1 org";
    }else if(S.bscope==="team"){
      rows=S.btree.teams.map((t,i)=>budgetRow(t.name,teamSpent(t),t.cap,t.agents.length+" agents","T",i)).join("");
      $(root,"[data-bcount]").textContent=S.btree.teams.length+" teams";
    }else{
      const ags=allAgents();
      rows=ags.map((a,i)=>budgetRow(a.name,a.spent,a.cap,a.team,"A",i,a.flagged)).join("");
      $(root,"[data-bcount]").textContent=ags.length+" agents";
    }
    $(root,"[data-budgets]").innerHTML=rows;
  }
  function renderBudgetDet(){
    const sel=S.bsel;if(!sel)return;
    let name,spent,cap,scopeLabel,kids=null,leaf=null;
    if(sel.scope==="org"){const o=S.btree.org;name=o.name;spent=orgSpent();cap=o.cap;scopeLabel="org";
      kids=S.btree.teams.map(t=>({name:t.name,spent:teamSpent(t),cap:t.cap,tag:"T"}));}
    else if(sel.scope==="team"){const t=S.btree.teams[sel.i];name=t.name;spent=teamSpent(t);cap=t.cap;scopeLabel="team";
      kids=t.agents.map(a=>({name:a.name,spent:a.spent,cap:a.cap,tag:"A",flagged:a.flagged}));}
    else{leaf=allAgents()[sel.i];name=leaf.name;spent=leaf.spent;cap=leaf.cap;scopeLabel="agent · "+leaf.team;}
    const over=cap?spent/cap:0, cls=over>=.95?"ember":over>=.8?"amber":"mint";
    $(root,"[data-bdid]").textContent=name;
    const p=$(root,"[data-bdpill]"),pv=over>=1?["crit","over cap"]:over>=.95?["crit","95%"]:over>=.8?["near","80%"]:["live","within cap"];
    p.className="lm-pill "+pv[0];p.textContent=pv[1];
    $(root,"[data-bdcap]").textContent=scopeLabel+" spend";
    const amt=$(root,"[data-bdamt]");amt.textContent="$"+f2(spent);amt.style.color=over>=1?"var(--ember)":"var(--fg)";
    $(root,"[data-bdof]").innerHTML="of <b>$"+cap.toFixed(2)+"</b> cap · "+Math.round(over*100)+"% · 80% warn / 95% alert";
    const bf=$(root,"[data-bdfuse]");bf.className="lm-fuse "+cls;$(bf,"i").style.width=Math.min(104,over*100)+"%";
    const kidsEl=$(root,"[data-bdkids]");
    if(leaf){
      $(root,"[data-bdlabel]").textContent="This agent";
      kidsEl.innerHTML=`<div class="lm-chainrow" style="line-height:1.5">This cap applies to every run the agent opens; the fuse trips and the gateway returns 402 at the cap.</div>`
        +(leaf.flagged?`<button class="lm-flag" data-goto-behaviour="${leaf.name}" style="margin-top:10px"><span class="fi"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M4 21V4h11l-1.5 3.5L15 11H4"/></svg></span><span class="ft"><b>Flagged: ${leaf.flagged}</b><span>open the behaviour detail</span></span><span class="fg">›</span></button>`:"");
    }else{
      $(root,"[data-bdlabel]").textContent="Breakdown";
      kidsEl.innerHTML=kids.map(k=>{const ov=k.cap?k.spent/k.cap:0,kc=ov>=.95?"ember":ov>=.8?"amber":"mint";
        return `<div class="lm-run" style="cursor:default">
          <div class="bd">${k.tag}</div>
          <div class="mid">
            <div class="idrow"><span class="id">${k.name}</span>${k.flagged?`<span class="lm-pill near">${k.flagged}</span>`:`<span class="lm-pill ${ov>=1?"crit":ov>=.8?"near":"live"}">${ov>=1?"over":ov>=.8?"warn":"ok"}</span>`}<span class="rt" style="color:var(--dim)">${Math.round(ov*100)}%</span></div>
            <div class="money"><span></span><span><b>$${f2(k.spent)}</b> / $${k.cap.toFixed(2)}</span></div>
            <div class="lm-fuse ${kc}"><i style="width:${Math.min(104,ov*100)}%"></i></div>
          </div></div>`;}).join("");
    }
  }
  function renderAgents(){
    const rank=s=>s==="crit"?3:s==="near"?2:1;
    let list=S.agents.slice();
    if(S.asort==="risk")list.sort((a,b)=>rank(b.sev)-rank(a.sev)||b.blast-a.blast);
    $(root,"[data-acount]").textContent=S.agents.length+" flagged";
    $(root,"[data-agents]").innerHTML=list.map(a=>{const i=S.agents.indexOf(a);
      return `<div class="lm-run ${a.sev==="crit"?"crit":""}" data-ai="${i}">
        <div class="bd" style="${a.sev==="crit"?"color:var(--ember);border-color:rgba(255,87,75,.4)":""}">${a.det[0].toUpperCase()}</div>
        <div class="mid">
          <div class="idrow"><span class="id">${a.id}</span><span class="lm-pill ${a.sev}">${a.det}</span><span class="rt" style="color:var(--dim)">${a.seen}</span></div>
          <div class="money" style="white-space:normal"><span style="color:var(--dim);line-height:1.4">${a.why}</span></div>
        </div></div>`;}).join("");
  }
  function renderAgentDet(){
    const a=S.agents[S.asel];if(!a)return;
    $(root,"[data-adid]").textContent=a.id;
    const p=$(root,"[data-adpill]");p.className="lm-pill "+a.sev;p.textContent=a.det;
    $(root,"[data-addet]").textContent=a.det.replace(/_/g," ");
    $(root,"[data-adwhy]").textContent=a.why;
    $(root,"[data-adchain]").textContent=a.chain==="—"?"none":a.chain.split("→").length+" deep";
    $(root,"[data-adblast]").textContent=a.blast;
    $(root,"[data-adseen]").textContent=a.seen;
    $(root,"[data-adchainrow]").textContent=a.chain;
  }
  function killRun(i,from){
    const r=S.runs[i];if(!r||r.st==="dead")return;
    r.st="dead";r.burn=0;
    renderRuns();renderWRuns();
    if(view==="detail")renderDetail();
    toast("Enclave-signed kill · gateway confirms · breaker open");
    if(from==="watch"){el.wkill.classList.add("done");$(el.wkill,"span").textContent="killed · 402";wshow("killed");}
    if(from==="phone"){ setTimeout(()=>{}, 0); }
  }

  /* run row -> detail */
  el.runs.addEventListener("click",e=>{const it=e.target.closest(".lm-run");if(!it)return;S.sel=+it.dataset.i;renderDetail();show("detail");});
  $(root,"[data-back]").addEventListener("click",()=>show("runs"));
  /* segmented filter */
  $(root,"[data-seg]").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;
    S.filter=b.dataset.f;$$(root,"[data-seg] button").forEach(x=>x.classList.toggle("on",x===b));renderRuns();});
  /* tab bar (delegated: the bar lives in several views now) */
  root.addEventListener("click",e=>{const b=e.target.closest("[data-tab]");if(!b)return;
    const t=b.dataset.tab;
    if(t==="runs")show("runs");
    else if(t==="alerts")show("push");
    else if(t==="budgets"){renderBudgets();show("budgets");}
    else if(t==="device")show("device");});
  /* runs -> flagged agents, agent row -> why, back buttons */
  $(root,"[data-goto-agents]").addEventListener("click",()=>{renderAgents();show("agents");});
  $(root,"[data-back-runs]").addEventListener("click",()=>show("runs"));
  $(root,"[data-back-agents]").addEventListener("click",()=>show("agents"));
  $(root,"[data-agents]").addEventListener("click",e=>{const it=e.target.closest("[data-ai]");if(!it)return;S.asel=+it.dataset.ai;renderAgentDet();show("agentdet");});
  /* segmented controls: budget scope, agent sort, remote-access mode */
  $(root,"[data-bseg]").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;S.bscope=b.dataset.b;$$(root,"[data-bseg] button").forEach(x=>x.classList.toggle("on",x===b));renderBudgets();});
  $(root,"[data-asort]").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;S.asort=b.dataset.s;$$(root,"[data-asort] button").forEach(x=>x.classList.toggle("on",x===b));renderAgents();});
  $(root,"[data-mseg]").addEventListener("click",e=>{const b=e.target.closest("button");if(!b)return;$$(root,"[data-mseg] button").forEach(x=>x.classList.toggle("on",x===b));
    $(root,"[data-mnote]").textContent=b.dataset.m==="strict"
      ?"Strict: the tunnel peer is revoked after a set window. Reconnecting needs a fresh code, obtainable on-network only."
      :"Phone stays paired; you toggle the tunnel off when done, and idle peers are dropped. Reconnect needs no new code.";});
  /* device disconnect + agent actions */
  $(root,"[data-disc]").addEventListener("click",()=>toast("device disconnected · a fresh pairing code would be needed"));
  /* device <-> pairing, with a code that visibly expires rather than sitting frozen */
  $(root,"[data-goto-pair]").addEventListener("click",()=>{resetTtl();show("pair");});
  $(root,"[data-back-device]").addEventListener("click",()=>show("device"));
  const ttlEl=$(root,"[data-pairttl]");let ttl=598;
  function paintTtl(){ttlEl.textContent=Math.floor(ttl/60)+":"+String(ttl%60).padStart(2,"0");}
  function resetTtl(){ttl=598;paintTtl();}
  setInterval(()=>{if(view!=="pair")return;ttl=ttl>0?ttl-1:598;paintTtl();},1000);
  $(root,"[data-throttle]").addEventListener("click",()=>toast("throttled · agent capped to its baseline rate"));
  $(root,"[data-agkill]").addEventListener("click",()=>toast("Enclave-signed kill · agent stopped across gateways"));
  /* budgets drill-in: scope row -> its breakdown -> (if flagged) behaviour */
  $(root,"[data-budgets]").addEventListener("click",e=>{const it=e.target.closest("[data-bi]");if(!it)return;
    S.bsel={scope:S.bscope,i:+it.dataset.bi};renderBudgetDet();show("budgetdet");});
  $(root,"[data-back-budgets]").addEventListener("click",()=>{renderBudgets();show("budgets");});
  $(root,"[data-bdkids]").addEventListener("click",e=>{const b=e.target.closest("[data-goto-behaviour]");if(!b)return;
    const idx=S.agents.findIndex(a=>a.id===b.dataset.gotoBehaviour);
    if(idx>=0){S.asel=idx;renderAgentDet();show("agentdet");}else{renderAgents();show("agents");}});

  /* Drag to scroll each screen. The page hijacks the mouse wheel, so a drag is
     what actually moves content out from under the tab bar. Taps still work: a
     click is only suppressed when the pointer actually moved.

     Deliberately NO setPointerCapture on the scroll box. With capture set, the
     browser dispatches pointerdown AND pointerup to the capturing element, so
     the click lands on the scroll box instead of whatever was tapped inside
     it: every control in a scrolling screen goes dead (the back arrows, the
     run/agent/budget rows), while the tab bar keeps working because it sits
     outside the scroll box. Tracking the drag on `window` instead keeps a drag
     alive past the frame edge without stealing the click. */
  let dragged=false;
  $$(root,".lm-scroll").forEach(sc=>{
    let down=false,sy=0,st=0,mv=0;
    const move=e=>{if(!down)return;const dy=e.clientY-sy;if(Math.abs(dy)>2)mv=Math.abs(dy);sc.scrollTop=st-dy;};
    const end=()=>{
      if(!down)return;
      if(mv>6){dragged=true;setTimeout(()=>{dragged=false;},140);}
      down=false;
      removeEventListener("pointermove",move);removeEventListener("pointerup",end);removeEventListener("pointercancel",end);
    };
    sc.addEventListener("pointerdown",e=>{
      if(e.target.closest("button,.lm-breaker"))return;
      down=true;sy=e.clientY;st=sc.scrollTop;mv=0;
      addEventListener("pointermove",move);addEventListener("pointerup",end);addEventListener("pointercancel",end);
    });
  });
  root.addEventListener("click",e=>{if(dragged){e.stopPropagation();e.preventDefault();}},true);
  /* expanded dynamic-island kill */
  $(root,"[data-dikill]").addEventListener("click",()=>{S.sel=0;killRun(0,"phone");toast("killed from the Dynamic Island");});
  /* push banners -> detail */
  $$(root,"[data-goto]").forEach(b=>b.addEventListener("click",()=>{S.sel=0;renderDetail();show("detail");}));

  /* watch switcher + kill */
  function wshow(w){$$(root,".lm-wview").forEach(x=>x.classList.toggle("on",x.dataset.w===w));
    $$(root,"[data-ws]").forEach(b=>b.classList.toggle("on",b.dataset.ws===w));}
  $(root,"[data-wswitch]").addEventListener("click",e=>{const b=e.target.closest("button");if(b)wshow(b.dataset.ws);});
  hold(el.wkill,900,()=>killRun(0,"watch"));

  /* live ticking */
  let t=0;
  setInterval(()=>{ t+=.4;
    S.runs.forEach(r=>{ if(r.st==="dead"){r.burn=0;return;}
      const wob=1+.05*Math.sin(t*1.6+r.cap);
      if(r.id==="7f3a2b"){ r.burn=1.9*wob; }
      else r.burn=Math.max(.02,r.burn*wob);
      r.spent+=r.burn/160;
    });
    const fb=S.runs.reduce((a,r)=>a+r.burn,0), overs=S.runs.filter(r=>r.st==="crit").length;
    el.fb.textContent=f2(fb);el.ftot.textContent="$"+f2(35.7+t*.01);
    $(el.ffuse,"i").style.width=Math.min(100,fb/2.4*100)+"%";
    el.diburn.textContent=f2(S.runs[0].st==="dead"?0:S.runs[0].burn);
    el.wface.innerHTML=f2(fb)+'<span class="cu"> $/m</span>';
    el.wfleet.innerHTML=f2(fb)+'<span class="cu"> $/m</span>';
    /* sparkline shifts */
    S.sparkV.push(0.35+Math.min(1,fb/2.6)*0.6+0.05*Math.sin(t*3));S.sparkV.shift();
    if(view==="runs"){spark(el.spark,S.sparkV,"#F4B23E");renderRuns();}
    if(view==="detail"&&S.runs[S.sel].st!=="dead")renderDetail();
  },400);

  /* Auto-cycling loop through the main screens (по колу), with the side steps
     as jump-in anchors. The loop pauses while you interact on-screen and then
     resumes, so every tab, slider and banner stays live. */
  const LOOP=["runs","detail","budgets","agents","pair","device","push"];
  const steps=stepsEl?[...stepsEl.querySelectorAll(".as-step")]:[];
  let loopI=0, pausedUntil=0;
  function goTo(i){
    loopI=((i%LOOP.length)+LOOP.length)%LOOP.length;
    const v=LOOP[loopI];
    if(v==="detail"){S.sel=0;renderDetail();}
    else if(v==="budgets")renderBudgets();
    else if(v==="agents")renderAgents();
    else if(v==="pair")resetTtl();
    show(v);
    steps.forEach((s,j)=>s.classList.toggle("on",j===loopI));
  }
  steps.forEach((s,i)=>{
    s.setAttribute("role","button");s.setAttribute("tabindex","0");
    const jump=()=>{goTo(i);pausedUntil=Date.now()+9000;};
    s.addEventListener("click",jump);
    s.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();jump();}});
  });
  /* any on-screen touch pauses the loop so it never yanks a screen mid-tap */
  const pause=e=>{if(!e.target.closest(".as-step"))pausedUntil=Date.now()+9000;};
  root.addEventListener("pointerdown",pause,true);
  root.addEventListener("click",pause,true);

  renderRuns();renderWRuns();renderDetail();renderBudgets();renderAgents();
  goTo(0);
  setInterval(()=>{if(Date.now()>=pausedUntil)goTo(loopI+1);},4200);
  requestAnimationFrame(()=>spark(el.spark,S.sparkV,"#F4B23E"));
  return {step:goTo};
}

/* =================================================================
   SPHERE: real iOS screenshots, navigable
   ================================================================= */
function sphere(root,stepsEl){
  ensureCss();
  const B="../assets/img/sphere/";
  const shots=[
    {img:"home-dark.png",  t:"The hub",     d:"All twelve spheres on one board."},
    {img:"health.png",     t:"Health",      d:"Sleep, training and vitals."},
    {img:"finance.png",    t:"Finance",     d:"Accounts, budgets, spending pattern."},
    {img:"goals.png",      t:"Goals",       d:"Long arcs broken into habits."},
    {img:"mindfulness-dark.png", t:"Mindfulness", d:"Mood and breathing sessions."},
    {img:"capture.png",    t:"Capture",     d:"One box for anything."}
  ];
  const wshots=[{img:"watch-home.png",t:"Glance"},{img:"watch-quicklog.png",t:"Quick log"}];
  root.classList.add("lm-wrap");
  root.innerHTML=
   `<figure class="lm-phone" style="margin:0"><span class="lm-island"></span>
     <div class="lm-shot" data-shot>
       ${shots.map((s,i)=>`<img src="${B}${s.img}" alt="${s.t}" ${i?'loading="lazy"':""} class="${i===0?"on":""}">`).join("")}
     </div>
   </figure>
   <div class="lm-watchcol">
     <figure class="lm-watch" style="margin:0"><span class="lm-crown"></span>
       <div class="lm-wscr lm-wshot" data-wshot>
         ${wshots.map((s,i)=>`<img src="${B}${s.img}" alt="${s.t}" loading="lazy" class="${i===0?"on":""}">`).join("")}
       </div>
     </figure>
     <div class="lm-wswitch" data-wswitch>
       ${wshots.map((s,i)=>`<button class="${i===0?"on":""}" data-wi="${i}">${s.t}</button>`).join("")}
     </div>
     <div class="lm-note">real captures from the iOS build</div>
   </div>`;
  const imgs=$$(root,"[data-shot] img"), wimgs=$$(root,"[data-wshot] img");
  function shot(i){imgs.forEach((im,j)=>im.classList.toggle("on",j===i));}
  function wshot(i){wimgs.forEach((im,j)=>im.classList.toggle("on",j===i));
    $$(root,"[data-wswitch] button").forEach((b,j)=>b.classList.toggle("on",j===i));}
  /* tap the phone to advance */
  let cur=0;
  $(root,".lm-phone").addEventListener("click",()=>{cur=(cur+1)%imgs.length;shot(cur);
    const st=stepsEl&&[...stepsEl.querySelectorAll(".as-step")];if(st)st.forEach((s,j)=>s.classList.toggle("on",j===cur));});
  $(root,"[data-wswitch]").addEventListener("click",e=>{const b=e.target.closest("button");if(b)wshot(+b.dataset.wi);});
  wireSteps(stepsEl,i=>{cur=i;shot(i);});
  return {step:shot};
}

window.LiveMock={pocket,sphere};
})();
