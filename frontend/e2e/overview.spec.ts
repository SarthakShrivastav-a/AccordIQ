import { expect, test } from "@playwright/test";

test("unauthenticated overview redirects to login", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Continue with Google")).toBeVisible();
});

test("login page renders", async ({ page }) => {
  await page.goto("/login");
  await expect(page.getByText("AccordIQ")).toBeVisible();
  await expect(page.getByText("Continue with Google")).toBeVisible();
});
