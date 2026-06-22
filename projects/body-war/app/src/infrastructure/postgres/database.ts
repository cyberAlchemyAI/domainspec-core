import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import { bodyWarSchema } from "./schema.js";

export type BodyWarSqlClient = ReturnType<typeof postgres>;

const DEFAULT_DATABASE_URL =
  "postgres://body_war_e2e:body_war_e2e_password@127.0.0.1:55433/body_war_e2e";

export function defaultBodyWarDatabaseUrl(): string {
  return process.env.BODY_WAR_DATABASE_URL ??
    process.env.DATABASE_URL ??
    DEFAULT_DATABASE_URL;
}

export function createBodyWarSqlClient(
  databaseUrl = defaultBodyWarDatabaseUrl(),
): BodyWarSqlClient {
  return postgres(databaseUrl, {
    connect_timeout: 10,
    idle_timeout: 5,
    max: 1,
    onnotice: () => undefined,
  });
}

export function createBodyWarDatabase(sql: BodyWarSqlClient) {
  return drizzle(sql, { schema: bodyWarSchema });
}

export async function closeBodyWarSqlClient(
  sql: BodyWarSqlClient,
): Promise<void> {
  await sql.end({ timeout: 5 });
}
