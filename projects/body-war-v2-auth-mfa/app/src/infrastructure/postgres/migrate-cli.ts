import {
  closeBodyWarSqlClient,
  createBodyWarSqlClient,
  defaultBodyWarDatabaseUrl,
} from "./database.js";
import { applyBodyWarMigrations } from "./migrations.js";

const sql = createBodyWarSqlClient(defaultBodyWarDatabaseUrl());

try {
  await applyBodyWarMigrations(sql);
} finally {
  await closeBodyWarSqlClient(sql);
}
