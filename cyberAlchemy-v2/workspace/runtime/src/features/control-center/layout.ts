export type WorkspaceSurface = "explore" | "foundation" | "ontology" | "essays" | "chat";

/** Layout is presentation only; it never changes conversation intent or authority. */
export function isSurfaceVisible(candidate: WorkspaceSurface, selected: WorkspaceSurface, docked: boolean): boolean {
  return candidate === selected || (docked && candidate === "chat");
}
