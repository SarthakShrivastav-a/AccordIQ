import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Badge } from "./Badge";

describe("Badge", () => {
  it("renders status text", () => {
    render(<Badge tone="good">connected</Badge>);
    expect(screen.getByText("connected")).toBeInTheDocument();
  });
});
