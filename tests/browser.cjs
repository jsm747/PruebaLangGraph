// Optional browser regression: run against an isolated local server.
// Requires Node.js, Playwright and a Chromium installation; see README.md.
const { chromium } = require('playwright');

(async () => {
  const base = process.env.APF_TEST_URL || 'http://127.0.0.1:8000';
  const options = { headless: true };
  if (process.env.APF_CHROMIUM_PATH) options.executablePath = process.env.APF_CHROMIUM_PATH;
  const browser = await chromium.launch(options);
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 950 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('dialog', async dialog => { errors.push(dialog.message()); await dialog.dismiss(); });
    await page.goto(base + '/tasks', { waitUntil: 'networkidle' });
    const title = 'Prueba sintética ' + Array.from(require('crypto').randomBytes(8), n => String.fromCharCode(97 + n % 26)).join('');
    await page.locator('#title').fill(title);
    await page.locator('#description').fill('Preparar un borrador para revisión.');
    await page.locator('#criteria').fill('Debe incluir criterios\nDebe ser sintético');
    await page.getByRole('button', { name: 'Crear propuesta' }).click();
    await page.locator('#detail').getByText('Pendiente de revisión', { exact: true }).waitFor();
    for (const name of ['append-only', 'citations', 'layer', 'scope']) {
      await page.locator('#detail').getByText(name + ': correcta', { exact: false }).waitFor();
    }
    await page.locator('#note').fill('Añadir contexto sintético');
    await page.getByRole('button', { name: 'Solicitar cambio' }).click();
    await page.locator('.proposal:not(.diff)').getByText('Añadir contexto sintético', { exact: false }).waitFor();
    await page.getByRole('button', { name: 'Aprobar propuesta' }).click();
    await page.locator('#detail').getByText('Integrada', { exact: true }).waitFor();
    const artifacts = await (await page.request.get(base + '/api/artifacts')).json();
    if (!artifacts.some(a => a.content.includes(title) && a.content.includes('Añadir contexto sintético'))) {
      throw new Error('No se encontró el artefacto aprobado.');
    }
    await page.locator('#title').fill('Alcance rechazado');
    await page.locator('#description').fill('Caso sintético.');
    await page.locator('summary').click();
    await page.locator('#scope').fill('instances/readiness-test/spec/no-permitido.md');
    await page.getByRole('button', { name: 'Crear propuesta' }).click();
    await page.locator('#detail').getByText('layer: fallida', { exact: false }).waitFor();
    if (!(await page.getByRole('button', { name: 'Aprobar propuesta' }).isDisabled())) {
      throw new Error('La interfaz permite aprobar con un control en rojo.');
    }
    if (errors.length) throw new Error(errors.join('; '));
    const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await mobile.goto(base, { waitUntil: 'networkidle' });
    if (await mobile.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) {
      throw new Error('Desbordamiento horizontal en móvil.');
    }
    console.log('Navegador: propuesta, cambio, aprobación, control rojo y vista móvil correctos.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
