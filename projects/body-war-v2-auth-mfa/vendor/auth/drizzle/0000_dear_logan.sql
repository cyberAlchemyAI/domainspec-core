CREATE TYPE "public"."grantee_type" AS ENUM('role', 'principal');--> statement-breakpoint
CREATE TYPE "public"."permission_effect" AS ENUM('ALLOW', 'DENY');--> statement-breakpoint
CREATE TYPE "public"."principal_status" AS ENUM('ACTIVE', 'DISABLED');--> statement-breakpoint
CREATE TYPE "public"."principal_subject_type" AS ENUM('user', 'service', 'automation');--> statement-breakpoint
CREATE TYPE "public"."session_status" AS ENUM('ACTIVE', 'TERMINATED', 'EXPIRED');--> statement-breakpoint
CREATE TABLE "auth_access_tokens" (
	"token_id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"session_id" uuid NOT NULL,
	"issued_at" timestamp DEFAULT now() NOT NULL,
	"expires_at" timestamp NOT NULL,
	"revoked_at" timestamp,
	"revoke_reason" varchar(100),
	"scope" jsonb DEFAULT '[]'::jsonb NOT NULL
);
--> statement-breakpoint
CREATE TABLE "auth_permission_grants" (
	"grant_id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"grantee_type" "grantee_type" NOT NULL,
	"grantee_key" varchar(255) NOT NULL,
	"permission_key" varchar(255) NOT NULL,
	"effect" "permission_effect" DEFAULT 'ALLOW' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "auth_principals" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"identifier" varchar(255) NOT NULL,
	"subject_type" "principal_subject_type" NOT NULL,
	"status" "principal_status" DEFAULT 'ACTIVE' NOT NULL,
	"role_keys" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"direct_permissions" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"credential_hash" varchar(255) NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL,
	CONSTRAINT "auth_principals_identifier_unique" UNIQUE("identifier")
);
--> statement-breakpoint
CREATE TABLE "auth_sessions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"principal_id" uuid NOT NULL,
	"status" "session_status" DEFAULT 'ACTIVE' NOT NULL,
	"effective_permissions" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"expires_at" timestamp NOT NULL
);
--> statement-breakpoint
ALTER TABLE "auth_access_tokens" ADD CONSTRAINT "auth_access_tokens_session_id_auth_sessions_id_fk" FOREIGN KEY ("session_id") REFERENCES "public"."auth_sessions"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "auth_sessions" ADD CONSTRAINT "auth_sessions_principal_id_auth_principals_id_fk" FOREIGN KEY ("principal_id") REFERENCES "public"."auth_principals"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE UNIQUE INDEX "auth_permission_grants_unique_grant" ON "auth_permission_grants" USING btree ("grantee_type","grantee_key","permission_key");