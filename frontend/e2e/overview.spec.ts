import { expect, test } from "@playwright/test";

test("overview renders without going blank", async ({ page }) => {
      await page.goto("/");
      await expect(page.getByText("Team memory, under control.")).toBeVisible();
      await expect(page.getByRole("main").getByText("Workspaces")).toBeVisible();
    });

test("query playground renders", async ({ page }) => {
  await page.goto("/query");
  await expect(page.getByText("Ask the memory.")).toBeVisible();
});
