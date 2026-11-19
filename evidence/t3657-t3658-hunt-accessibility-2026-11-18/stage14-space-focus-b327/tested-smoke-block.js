    // Space is mode-scoped: it ascends in the air and inspects on foot. If that
    // ever leaks, walking visitors levitate every time they try to inspect.
    await page.evaluate(() => {
      window.__chicago4d.goTo('sauganash');
      // Aim at the building, the same way the pick test does — Space inspects
      // down the crosshair, so a test that has not aimed is testing the prairie.
      window.__chicago4d.frame('sauganash_hotel', 26);
    });
    // T-3614: a floating name card in the crosshair opens that person, which is right — and
    // the Sauganash's own household now stands at its door, Fullerton's card on the
    // crosshair. This check is about the key, not about who stands in front of the hotel,
    // so the name cards are put away for it and brought back after the toggle below.
    const namesShown = await page.evaluate(() => {
      const cards = window.__chicago4d.nameCards;
      const was = !!cards?.shown;
      cards?.setShown(false);
      return was;
    });
    // T-3022: what a visitor opens on a building opens in the Navigator's Inspect, not the
    // card; `api.inspecting` names the building on screen either way.
    // T-3638: a key is consumed inside a frame (main.js tick → intent.takeInteract), and the
    // crosshair it inspects down is the camera the LAST frame left. Under SwiftShader a frame
    // can take seconds, so a fixed wait read the scene before any frame had run — or had the
    // raycast fired from the camera before `frame()` aimed it — and the check went red on
    // whichever viewport the runner happened to starve (dev 44076624959 mobile and desktop,
    // 44193370202 desktop only). One forced frame settles the aim, and one after each key
    // consumes it, so what is read is what the key did. `stepKey` is the same `api.step()`
    // the click check below has always used; it never waits any less than before.
    const stepKey = async (key, ms, worldFocus = '') => {
      if (worldFocus) {
        // T-3658: closing a reader focuses its reopening control. Camera-only
        // goTo/frame calls do not return the keyboard to the world. Establish
        // this precondition explicitly; focused UI must retain its native keys.
        const focus = await page.evaluate(() => {
          const before = document.activeElement;
          const from = `${before?.tagName ?? 'none'}#${before?.id ?? ''}`;
          before?.blur?.();
          const after = document.activeElement;
          return { from, to: `${after?.tagName ?? 'none'}#${after?.id ?? ''}`,
            world: after === document.body || after?.tagName === 'CANVAS' };
        });
        check(`${label}: ${worldFocus} has world keyboard focus`, focus.world,
          `${focus.from} → ${focus.to}`);
      }
      await page.keyboard.press(key);
      await page.waitForTimeout(ms);
      await page.evaluate(() => window.__chicago4d.step());
    };
    await page.evaluate(() => { window.__chicago4d.closeBuilding(); window.__chicago4d.step(); });
    // The complementary UI case is real native activation, not a swallowed key:
    // Space on the focused Navigator handle opens it without inspecting/moving.
    const uiSpaceBefore = await page.evaluate(async () => {
      const a = window.__chicago4d;
      await a.navigator.select('home');
      a.navigator.dock();
      const handle = ['nav-grip', 'nav-collapse'].map(id => document.getElementById(id))
        .find(el => el?.getClientRects().length && getComputedStyle(el).visibility !== 'hidden');
      handle?.focus({ preventScroll: true });
      return { e: a.player.e, n: a.player.n, focused: !!handle && document.activeElement === handle,
        focus: document.activeElement?.id, level: a.navigator.level };
    });
    await stepKey('Space', 250);
    const uiSpaceAfter = await page.evaluate(() => {
      const a = window.__chicago4d;
      return { e: a.player.e, n: a.player.n, flying: a.player.flying, inspected: !!a.inspecting,
        focus: document.activeElement?.id, level: a.navigator.level };
    });
    check(`${label}: Space activates a focused Navigator control without inspecting or moving`,
      uiSpaceBefore.focused && uiSpaceBefore.level === 0 && uiSpaceAfter.level > 0
      && !uiSpaceAfter.flying && !uiSpaceAfter.inspected
      && Math.hypot(uiSpaceAfter.e - uiSpaceBefore.e, uiSpaceAfter.n - uiSpaceBefore.n) < 0.05,
      `${uiSpaceBefore.focus} → ${uiSpaceAfter.focus}, level ${uiSpaceAfter.level}, inspected ${uiSpaceAfter.inspected}`);
    await page.evaluate(() => window.__chicago4d.navigator.dock());
    await stepKey('Space', 250, 'on-foot Space');
    const spaceOnFoot = await page.evaluate(() => ({
      alt: window.__chicago4d.player.altitude,
      flying: window.__chicago4d.player.flying,
      inspected: !!window.__chicago4d.inspecting,
    }));
    check(`${label}: Space inspects on foot instead of lifting off`,
      spaceOnFoot.flying === false && Math.abs(spaceOnFoot.alt) < 0.2 && spaceOnFoot.inspected,
      `flying ${spaceOnFoot.flying}, ${spaceOnFoot.alt?.toFixed(2)} m up, inspected ${spaceOnFoot.inspected}`);

    // --- the keys that close the card (T-0108) -------------------------------
    //
    // Owner-reported: nothing closed an inspection card from the keyboard —
    // the only way out was scrolling up to its close button. Escape closes,
    // and the inspect key toggles: the reach that opened the card also closes
    // it. Escape is the browser's own pointer-lock release, which the handler
    // cooperates with by acting only when a card is open; there is no lock in
    // this harness, so the keystroke reaches the page directly. The card is
    // open right now, left by the Space assertion above.
    await page.keyboard.press('Escape');
    await page.waitForTimeout(150);
    const escClosed = await page.evaluate(() => !window.__chicago4d.inspecting);
    check(`${label}: Escape closes the inspection card`, escClosed,
      `card hidden after Escape: ${escClosed}`);

    await stepKey('Space', 300, 'Space reopening the card'); // same crosshair, reopens
    const reopened = await page.evaluate(() => !!window.__chicago4d.inspecting);
    await stepKey('KeyE', 300);
    const keyToggled = await page.evaluate(() => !window.__chicago4d.inspecting);
    check(`${label}: the inspect key closes the card it opened`,
      reopened && keyToggled,
      `reopened ${reopened}, closed by the same key ${keyToggled}`);
    await page.evaluate((was) => window.__chicago4d.nameCards?.setShown(was), namesShown);

