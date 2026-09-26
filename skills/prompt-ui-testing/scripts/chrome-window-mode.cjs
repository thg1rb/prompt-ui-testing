async function waitForStableWindow(page, session) {
  const timeout = 5000;
  const stableFor = 700;
  const pollInterval = 100;
  const startedAt = Date.now();
  let stableSince = startedAt;
  let previous = null;
  let latest;

  while (Date.now() - startedAt < timeout) {
    const { bounds } = await session.send('Browser.getWindowForTarget');
    const viewport = await page.evaluate(() => ({
      innerWidth,
      innerHeight,
      outerWidth,
      outerHeight,
      screenWidth: screen.width,
      screenHeight: screen.height,
    }));
    latest = { bounds, viewport };
    const current = JSON.stringify(latest);

    if (current !== previous) {
      previous = current;
      stableSince = Date.now();
    } else if (Date.now() - stableSince >= stableFor) {
      return { ...latest, stable: true };
    }

    await new Promise((resolve) => setTimeout(resolve, pollInterval));
  }

  return { ...latest, stable: false };
}

module.exports.default = async ({ page }) => {
  let session;
  let windowMode = 'unverified';

  try {
    const isHeadless = await page.evaluate(() => navigator.userAgent.includes('HeadlessChrome/'));
    if (isHeadless) {
      windowMode = 'headless';
    } else {
      session = await page.context().newCDPSession(page);
      const { windowId } = await session.send('Browser.getWindowForTarget');

      try {
        await session.send('Browser.setWindowBounds', {
          windowId,
          bounds: { windowState: 'maximized' },
        });
        await waitForStableWindow(page, session);
      } catch {
        // Fullscreen is still attempted if the maximized preparation fails.
      }

      try {
        await session.send('Browser.setWindowBounds', {
          windowId,
          bounds: { windowState: 'fullscreen' },
        });
      } catch {
        // A failed Fullscreen request still gets a maximized fallback attempt.
      }

      let settled = await waitForStableWindow(page, session);
      if (settled.stable && settled.bounds.windowState === 'fullscreen') {
        windowMode = 'fullscreen';
      } else {
        await session.send('Browser.setWindowBounds', {
          windowId,
          bounds: { windowState: 'maximized' },
        });
        settled = await waitForStableWindow(page, session);
        windowMode = settled.stable && settled.bounds.windowState === 'maximized'
          ? 'maximized-fallback'
          : 'unverified';
      }
    }
  } catch {
    windowMode = 'unverified';
  } finally {
    try {
      await session?.detach();
    } catch {
      // A detached browser session must not prevent testing from continuing.
    }
  }

  await page.evaluate((mode) => {
    const message = `[prompt-ui-testing] Browser window mode: ${mode}`;
    if (mode === 'maximized-fallback') console.warn(message);
    else if (mode === 'unverified') console.error(message);
    else console.info(message);
  }, windowMode).catch(() => {});
};
