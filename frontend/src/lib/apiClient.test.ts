import { afterEach, describe, expect, it, vi } from "vitest";
import { apiClient, clearAccessToken, setAccessToken } from "./apiClient";

describe("apiClient", () => {
  afterEach(() => {
    clearAccessToken();
    vi.unstubAllGlobals();
  });

  it("sends the JWT bearer token", async () => {
    setAccessToken("jwt-token");
    const fetchMock = vi.fn(() => Promise.resolve(new Response(JSON.stringify({ items: [] }), { status: 200 })));
    vi.stubGlobal("fetch", fetchMock);
    const data = await apiClient.workspaces();
    expect(data.items).toEqual([]);
    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/api/admin/workspaces", expect.objectContaining({ headers: expect.objectContaining({ Authorization: "Bearer jwt-token" }) }));
  });

  it("does not return fallback data when backend fails", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("offline"))));
    await expect(apiClient.workspaces()).rejects.toThrow("offline");
  });
});
