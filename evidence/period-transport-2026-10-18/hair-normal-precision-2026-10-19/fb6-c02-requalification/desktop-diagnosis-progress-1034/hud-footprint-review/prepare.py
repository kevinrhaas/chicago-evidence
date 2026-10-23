from pathlib import Path
import difflib,hashlib,json
P=Path(__file__).parent;src=Path('/workspace/chicago/chicago/4d/tools/smoke_renderer.mjs');old=src.read_text();new=old
block='''      // dock() updates its detent synchronously, while the actual box still transitions.
      // After the hint wait, require the visible final dock immediately before sampling.
      const nav = document.getElementById('navigator'), deadline = performance.now() + 60000;
      const dockShown = (el) => {
        if (!el?.isConnected) return false;
        for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
          const cs = getComputedStyle(e);
          if (e.hidden || cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) < 0.05) return false;
        }
        return true;
      };
      let navigatorDock;
      do {
        const b = nav?.getBoundingClientRect(); // Flush style before reading native transitions.
        const phone = innerWidth <= 620;
        const animations = nav?.getAnimations?.() ?? [];
        navigatorDock = { detent: window.__chicago4d.navigator?.detent ?? null,
          level: window.__chicago4d.navigator?.level ?? null,
          box: b ? { x: b.x, y: b.y, width: b.width, height: b.height, right: b.right, bottom: b.bottom } : null,
          visible: dockShown(nav),
          running: animations.filter(a => a.playState === 'running' || a.pending).map(a => ({ state: a.playState, pending: a.pending, property: a.transitionProperty ?? null })) };
        navigatorDock.ready = !!b && navigatorDock.visible && b.height > 0
          && b.left >= 0 && b.top >= 0 && b.right <= innerWidth && b.bottom <= innerHeight
          && navigatorDock.level === 0 && navigatorDock.detent === (phone ? 'dock' : 'rail')
          && navigatorDock.running.length === 0
          && (phone ? Math.abs(b.width - 136) <= 1 && Math.abs(b.height - 64) <= 1 : Math.abs(b.width - 58) <= 1);
        if (navigatorDock.ready || performance.now() >= deadline) break;
        await new Promise(resolve => setTimeout(resolve, 100));
      } while (true);
'''
anchor="      const hintUp = !!document.getElementById('hint')?.classList.contains('on');\n";assert new.count(anchor)==1;new=new.replace(anchor,anchor+block,1)
needle="        controls: window.__chicago4d.controlBackend, lookTag:";assert new.count(needle)==1;new=new.replace(needle,"        navigatorDock, controls: window.__chicago4d.controlBackend, lookTag:",1)
needle='      footprints.every((f) => f.pct <= HUD_BUDGET_PCT && f.boxes > 0)';assert new.count(needle)==1;new=new.replace(needle,'      [...footprints, oneMore, oldRow].every((f) => f.navigatorDock.ready)\n      && footprints.every((f) => f.pct <= HUD_BUDGET_PCT && f.boxes > 0)',1)
(P/'smoke_renderer.mjs').write_text(new);(P/'revised-settle.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/chicago/4d/tools/smoke_renderer.mjs',tofile='b/chicago/4d/tools/smoke_renderer.mjs')))
(P/'source-hashes.json').write_text(json.dumps({'app_source_sha256':hashlib.sha256(old.encode()).hexdigest(),'proposed_source_sha256':hashlib.sha256(new.encode()).hexdigest(),'original_patch':'/workspace/shared/hud-footprint-f97-diagnosis/proposed-settle.patch','status':'outside only; no browser or app mutation'},indent=2)+'\n');print(hashlib.sha256((P/'revised-settle.patch').read_bytes()).hexdigest())
