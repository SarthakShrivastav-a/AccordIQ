import { describe, expect, it } from "vitest";
import { compactNumber, percent } from "./format";

describe("format helpers", () => {
  it("formats percentages", () => {
    expect(percent(0.91)).toBe("91%");
  });

  it("formats compact numbers", () => {
    expect(compactNumber(1200)).toContain("1");
  });
});
