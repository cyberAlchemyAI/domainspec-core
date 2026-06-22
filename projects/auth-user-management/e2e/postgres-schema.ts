import { readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import { authAccessControlSchema } from "../src/index.js";

export type E2eSqlClient = ReturnType<typeof postgres>;

const DEFAULT_PORT = "55432";
const MIGRATIONS_DIR = resolve(process.cwd(), "drizzle");

const DROP_AUTH_SCHEMA_SQL = [
  "drop table if exists auth_access_tokens",
  "drop table if exists auth_sessions",
  "drop table if exists auth_permission_grants",
  "drop table if exists auth_principals",
  "drop type if exists grantee_type",
  "drop type if exists permission_effect",
  "drop type if exists session_status",
  "drop type if exists principal_status",
  "drop type if exists principal_subject_type",
] as const;

export function defaultE2eDatabaseUrl(): string {
  const port = process.env.AUTH_E2E_POSTGRES_PORT ?? DEFAULT_PORT;
  return (
    process.env.AUTH_E2E_DATABASE_URL ??
    `postgres://auth_e2e:auth_e2e_password@127.0.0.1:${port}/auth_user_management_e2e`
  );
}

export function createE2eSqlClient(
  databaseUrl = defaultE2eDatabaseUrl(),
): E2eSqlClient {
  return postgres(databaseUrl, {
    connect_timeout: 10,
    idle_timeout: 5,
    max: 1,
    onnotice: () => undefined,
  });
}

export function createAuthDatabase(sql: E2eSqlClient) {
  return drizzle(sql, { schema: authAccessControlSchema });
}

export async function resetAuthSchema(sql: E2eSqlClient): Promise<void> {
  for (const statement of DROP_AUTH_SCHEMA_SQL) {
    await sql.unsafe(statement);
  }

  await applyGeneratedMigrations(sql);
}

export async function applyGeneratedMigrations(
  sql: E2eSqlClient,
): Promise<void> {
  await sql.unsafe("create extension if not exists pgcrypto");

  const migrationFiles = (await readdir(MIGRATIONS_DIR))
    .filter((file) => file.endsWith(".sql"))
    .sort();

  if (migrationFiles.length === 0) {
    throw new Error(`No generated Drizzle migrations found in ${MIGRATIONS_DIR}`);
  }

  for (const migrationFile of migrationFiles) {
    const migrationSql = await readFile(
      resolve(MIGRATIONS_DIR, migrationFile),
      "utf8",
    );

    for (const statement of splitDrizzleMigration(migrationSql)) {
      await sql.unsafe(statement);
    }
  }
}

function splitDrizzleMigration(migrationSql: string): string[] {
  return migrationSql
    .split("--> statement-breakpoint")
    .map((statement) => statement.trim())
    .filter((statement) => statement.length > 0);
}

export async function closeE2eSqlClient(
  sql: E2eSqlClient,
): Promise<void> {
  await sql.end({ timeout: 5 });
}
