const assert = require('node:assert/strict');
const test = require('node:test');
const configureWindowMode = require('../skills/prompt-ui-testing/scripts/chrome-window-mode.cjs').default;

function createPage({ fullscreenSupported = true, headless = false } = {}) {
  let state = 'normal';
  const requests = [];
  const messages = [];
  let sessionCreations = 0;
  const session = {
    async send(method, params) {
      requests.push({ method, params });
      if (method === 'Browser.getWindowForTarget') {
        return { windowId: 1, bounds: { windowState: state } };
      }
      if (method === 'Browser.setWindowBounds') {
        if (params.bounds.windowState !== 'fullscreen' || fullscreenSupported) {
          state = params.bounds.windowState;
        }
      }
      return {};
    },
    async detach() {},
  };
  const page = {
    context: () => ({
      newCDPSession: async () => {
        sessionCreations += 1;
        return session;
      },
    }),
    async evaluate(fn, value) {
      const source = fn.toString();
      if (value !== undefined) {
        messages.push(value);
        return;
      }
      if (source.includes('navigator.userAgent.includes')) return headless;
      if (source.includes('innerWidth') && source.includes('screenWidth')) {
        return {
          innerWidth: 1920,
          innerHeight: 992,
          outerWidth: 1920,
          outerHeight: 992,
          screenWidth: 1920,
          screenHeight: 1080,
        };
      }
      throw new Error(`Unexpected page evaluation: ${source}`);
    },
  };
  return { page, requests, messages, get sessionCreations() { return sessionCreations; } };
}

test('requests and reports Fullscreen when Chrome accepts it', async () => {
  const { page, requests, messages } = createPage();

  await configureWindowMode({ page });

  assert.equal(messages.at(-1), 'fullscreen');
  assert.deepEqual(
    requests.filter(({ method }) => method === 'Browser.setWindowBounds')
      .map(({ params }) => params.bounds.windowState),
    ['maximized', 'fullscreen'],
  );
});

test('uses and reports maximized fallback when Fullscreen is unavailable', async () => {
  const { page, requests, messages } = createPage({ fullscreenSupported: false });

  await configureWindowMode({ page });

  assert.equal(messages.at(-1), 'maximized-fallback');
  assert.deepEqual(
    requests.filter(({ method }) => method === 'Browser.setWindowBounds')
      .map(({ params }) => params.bounds.windowState),
    ['maximized', 'fullscreen', 'maximized'],
  );
});

test('reports an unverified mode when Chromium window control is unavailable', async () => {
  const messages = [];
  const page = {
    context: () => ({ newCDPSession: async () => { throw new Error('CDP unavailable'); } }),
    async evaluate(fn, value) {
      if (value === undefined && fn.toString().includes('navigator.userAgent.includes')) return false;
      messages.push(value);
    },
  };

  await configureWindowMode({ page });

  assert.deepEqual(messages, ['unverified']);
});

test('does not request or claim Fullscreen in headless mode', async () => {
  const { page, requests, messages, sessionCreations } = createPage({ headless: true });

  await configureWindowMode({ page });

  assert.equal(sessionCreations, 0);
  assert.deepEqual(requests, []);
  assert.deepEqual(messages, ['headless']);
});
