CREATE TYPE "public"."body_war_provider_status" AS ENUM('linked', 'disconnected');--> statement-breakpoint
CREATE TABLE "body_war_oauth_states" (
	"state" varchar(255) PRIMARY KEY NOT NULL,
	"nonce" varchar(255) NOT NULL,
	"redirect_target" varchar(500) DEFAULT '/' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"expires_at" timestamp NOT NULL,
	"consumed_at" timestamp
);
--> statement-breakpoint
CREATE TABLE "body_war_provider_accounts" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"principal_id" uuid NOT NULL,
	"provider" varchar(64) NOT NULL,
	"provider_user_id" varchar(255) NOT NULL,
	"display_name" varchar(255),
	"scope" jsonb DEFAULT '[]'::jsonb NOT NULL,
	"status" "body_war_provider_status" DEFAULT 'linked' NOT NULL,
	"metadata" jsonb DEFAULT '{}'::jsonb NOT NULL,
	"linked_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "body_war_provider_tokens" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"account_id" uuid NOT NULL,
	"access_token_ciphertext" varchar(2048) NOT NULL,
	"refresh_token_ciphertext" varchar(2048) NOT NULL,
	"expires_at" timestamp NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "body_war_runner_profiles" (
	"principal_id" uuid PRIMARY KEY NOT NULL,
	"display_name" varchar(255) NOT NULL,
	"privacy_status" varchar(64) DEFAULT 'private' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX "body_war_provider_unique_user" ON "body_war_provider_accounts" USING btree ("provider","provider_user_id");