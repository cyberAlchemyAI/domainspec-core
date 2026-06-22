import { readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";
import type { BodyWarSqlClient } from "./database.js";

const APP_ROOT = resolve(process.env.BODY_WAR_APP_ROOT ?? process.cwd());
const REPO_ROOT = resolve(APP_ROOT, "../..");
const AUTH_MIGRATIONS_DIR = resolve(REPO_ROOT, "auth-user-management/drizzle");
const BODY_WAR_MIGRATIONS_DIR = resolve(APP_ROOT, "drizzle");

const DROP_BODY_WAR_SQL = [
  "drop table if exists body_war_provider_tokens",
  "drop table if exists body_war_provider_accounts",
  "drop table if exists body_war_oauth_states",
  "drop table if exists body_war_runner_profiles",
  "drop type if exists body_war_provider_status",
] as const;

const DROP_AUTH_SQL = [
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

export async function resetBodyWarDatabase(sql: BodyWarSqlClient): Promise<void> {
  for (const statement of DROP_BODY_WAR_SQL) {
    await sql.unsafe(statement);
  }
  for (const statement of DROP_AUTH_SQL) {
    await sql.unsafe(statement);
  }
  await applyBodyWarMigrations(sql);
}

export async function applyBodyWarMigrations(
  sql: BodyWarSqlClient,
): Promise<void> {
  await sql.unsafe("create extension if not exists pgcrypto");
  await applySqlDirectory(sql, AUTH_MIGRATIONS_DIR);
  await applySqlDirectory(sql, BODY_WAR_MIGRATIONS_DIR);
}

async function applySqlDirectory(
  sql: BodyWarSqlClient,
  migrationsDir: string,
): Promise<void> {
  const migrationFiles = (await readdir(migrationsDir))
    .filter((file) => file.endsWith(".sql"))
    .sort();

  if (migrationFiles.length === 0) {
    throw new Error(`No generated Drizzle migrations found in ${migrationsDir}`);
  }

  for (const migrationFile of migrationFiles) {
    const migrationSql = await readFile(resolve(migrationsDir, migrationFile), "utf8");
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
