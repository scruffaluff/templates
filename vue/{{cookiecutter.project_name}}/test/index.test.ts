/**
 * High level application end to end tests.
 */

import { expect, test } from "@playwright/test";

test("Webpage title matches application name", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveTitle("{{ cookiecutter.project_name }}");
});
