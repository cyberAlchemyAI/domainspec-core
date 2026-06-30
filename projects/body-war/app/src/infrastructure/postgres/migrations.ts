import { createHash } from "node:crypto";
import { readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";
import type { BodyWarSqlClient } from "./database.js";

const APP_ROOT = resolve(process.env.BODY_WAR_APP_ROOT ?? process.cwd());
const REPO_ROOT = resolve(APP_ROOT, "../..");
const AUTH_MIGRATIONS_DIR = resolve(REPO_ROOT, "auth-user-management/drizzle");
const BODY_WAR_MIGRATIONS_DIR = resolve(APP_ROOT, "drizzle");
const MIGRATION_LOCK_ID = 51740001;
const MIGRATION_LEDGER_TABLE_SQL = `
create table if not exists body_war_schema_migrations (
  scope varchar(100) not null,
  filename varchar(255) not null,
  checksum varchar(64) not null,
  applied_at timestamp default now() not null,
  primary key (scope, filename)
)`;
const IGNORABLE_DUPLICATE_SQLSTATE: readonly string[] = ["42710", "42P07"];

const DROP_BODY_WAR_SQL = [
  "drop table if exists body_war_activity_evidence_candidates",
  "drop table if exists body_war_suggested_tracks",
  "drop table if exists body_war_provider_tokens",
  "drop table if exists body_war_provider_accounts",
  "drop table if exists body_war_oauth_states",
  "drop table if exists body_war_runner_profiles",
  "drop type if exists body_war_activity_evidence_candidate_status",
  "drop type if exists body_war_suggested_track_status",
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
  await sql.unsafe("drop table if exists body_war_schema_migrations");
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
  await sql`select pg_advisory_lock(${MIGRATION_LOCK_ID})`;
  try {
    await sql.unsafe("create extension if not exists pgcrypto");
    await sql.unsafe(MIGRATION_LEDGER_TABLE_SQL);
    await applySqlDirectory(sql, "auth-user-management", AUTH_MIGRATIONS_DIR);
    await applySqlDirectory(sql, "body-war", BODY_WAR_MIGRATIONS_DIR);
  } finally {
    await sql`select pg_advisory_unlock(${MIGRATION_LOCK_ID})`;
  }
}

async function applySqlDirectory(
  sql: BodyWarSqlClient,
  scope: string,
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
    const checksum = createMigrationChecksum(migrationSql);
    const existingMigrations = await sql<{ checksum: string }[]>`
      select checksum
      from body_war_schema_migrations
      where scope = ${scope}
        and filename = ${migrationFile}
      limit 1
    `;

    const existingMigration = existingMigrations[0];
    if (existingMigration !== undefined) {
      if (existingMigration.checksum !== checksum) {
        throw new Error(
          `Migration checksum mismatch for ${scope}/${migrationFile}`,
        );
      }
      continue;
    }

    for (const statement of splitDrizzleMigration(migrationSql)) {
      await applyMigrationStatement(sql, statement);
    }

    await sql`
      insert into body_war_schema_migrations (scope, filename, checksum)
      values (${scope}, ${migrationFile}, ${checksum})
    `;
  }
}

async function applyMigrationStatement(
  sql: BodyWarSqlClient,
  statement: string,
): Promise<void> {
  try {
    await sql.unsafe(statement);
  } catch (error) {
    if (isIgnorableDuplicateMigrationError(error)) {
      return;
    }
    throw error;
  }
}

function createMigrationChecksum(migrationSql: string): string {
  return createHash("sha256").update(migrationSql).digest("hex");
}

function isIgnorableDuplicateMigrationError(error: unknown): boolean {
  const postgresError = error as { code?: unknown };
  return typeof postgresError.code === "string" &&
    IGNORABLE_DUPLICATE_SQLSTATE.includes(postgresError.code);
}

function splitDrizzleMigration(migrationSql: string): string[] {
  return migrationSql
    .split("--> statement-breakpoint")
    .map((statement) => statement.trim())
    .filter((statement) => statement.length > 0);
}
