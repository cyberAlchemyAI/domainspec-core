import { createHash } from "node:crypto";

type ObjectValue = Record<string, any>;
function requireValue(ok: unknown, message: string): asserts ok { if (!ok) throw Error(message); }
const finite = (n: unknown): n is number => typeof n === "number" && Number.isFinite(n);

// This checks recorded evidence consistency, not Strava authenticity or permission.
export function qualifyGeometryExport(geoBytes: string, reportBytes: string) {
  const geo: ObjectValue = JSON.parse(geoBytes), report: ObjectValue = JSON.parse(reportBytes);
  const meta = geo.body_war_export;
  requireValue(geo.type === "FeatureCollection" && meta?.schema === "body-war-strava-geometry-export/v1", "invalid_export_schema");
  requireValue(report.schema === meta.schema && report.source === "strava_activity_streams" && meta.source === report.source, "invalid_export_source");
  requireValue(typeof meta.generated_at === "string" && Number.isFinite(Date.parse(meta.generated_at)) && report.generated_at === meta.generated_at, "invalid_export_time");
  requireValue(Array.isArray(geo.features) && geo.features.length > 0 && geo.features.length <= 300, "invalid_feature_count");
  requireValue(report.exported_activity_count === geo.features.length && meta.exported_activity_count === geo.features.length, "export_count_mismatch");
  requireValue(Array.isArray(report.outcomes), "missing_export_outcomes");
  const refs = new Set<string>();
  let points = 0;
  for (const feature of geo.features) {
    const p = feature.properties, coordinates = feature.geometry?.coordinates;
    requireValue(feature.type === "Feature" && feature.geometry?.type === "LineString" && p?.provider === "strava", "invalid_feature");
    requireValue(typeof p.source_activity_ref === "string" && /^[a-f0-9]{24}$/.test(p.source_activity_ref) && !refs.has(p.source_activity_ref), "invalid_activity_reference");
    refs.add(p.source_activity_ref);
    requireValue(Array.isArray(coordinates) && coordinates.length >= 2 && coordinates.length <= 1000000, "invalid_coordinate_count");
    requireValue(p.point_count === coordinates.length, "point_count_mismatch");
    requireValue(coordinates.every((c: unknown) => Array.isArray(c) && c.length === 2 && finite(c[0]) && finite(c[1]) && Math.abs(c[0]) <= 180 && Math.abs(c[1]) <= 90), "invalid_coordinates");
    for (const [key, last] of [["coordinate_distances_meters", "stream_distance_meters"], ["coordinate_times_seconds", "elapsed_seconds"]]) {
      const values = p[key!];
      requireValue(Array.isArray(values) && values.length === coordinates.length, "stream_length_mismatch");
      requireValue(values.every((v: unknown, i: number) => finite(v) && v >= 0 && (i === 0 || v >= values[i-1])), "nonmonotonic_stream");
      requireValue(values.at(-1) === p[last!] && p[last!] > 0, "stream_total_mismatch");
    }
    const outcomes = report.outcomes.filter((o: ObjectValue) => o.source_activity_ref === p.source_activity_ref);
    requireValue(outcomes.length === 1 && outcomes[0].status === "exported" && outcomes[0].point_count === coordinates.length, "export_outcome_mismatch");
    points += coordinates.length;
  }
  return {status: "structurally-qualified", activities: refs.size, points, generated_at: meta.generated_at,
    geometry_sha256: createHash("sha256").update(geoBytes).digest("hex"), report_sha256: createHash("sha256").update(reportBytes).digest("hex"),
    authenticity: "requires-source-provenance", athlete_permission: "requires-owner-confirmation", live_provider: "not-tested"};
}
