import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
      testDir: "./e2e",
      webServer: {
        command: "npm run dev -- --port 3100",
        url: "http://127.0.0.1:3100",
        reuseExistingServer: false,
        timeout: 120000
      },
      use: {
        baseURL: "http://127.0.0.1:3100",
        trace: "on-first-retry"
      },
  projects: [
    { name: "chrome", use: { ...devices["Desktop Chrome"], channel: "chrome" } },
    { name: "mobile-chrome", use: { ...devices["Pixel 7"], channel: "chrome" } }
  ]
});
