import { describe, expect, it, vi } from "vitest";
import { apiClient } from "./apiClient";

describe("apiClient", () => {
  it("falls back to demo data when backend is unavailable", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("offline"))));
    const data = await apiClient.workspaces();
    expect(data.items.length).toBeGreaterThan(0);
    vi.unstubAllGlobals();
  });
});
