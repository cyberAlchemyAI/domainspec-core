import { describe, expect, it } from "vitest";
import { isSurfaceVisible, type WorkspaceSurface } from "./layout";

const surfaces: WorkspaceSurface[] = ["explore", "foundation", "ontology", "essays", "chat"];
describe("control center visibility", () => {
  for (const selected of surfaces) {
    it(`preserves normal navigation to ${selected}`, () => {
      expect(surfaces.filter(s => isSurfaceVisible(s, selected, false))).toEqual([selected]);
    });
    it(`retains one chat alongside ${selected}`, () => {
      expect(surfaces.filter(s => isSurfaceVisible(s, selected, true))).toEqual(
        surfaces.filter(s => s === selected || s === "chat"),
      );
    });
  }
});
