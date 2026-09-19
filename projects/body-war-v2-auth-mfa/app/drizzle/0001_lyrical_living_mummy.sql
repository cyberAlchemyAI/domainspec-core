CREATE TYPE "public"."body_war_activity_evidence_candidate_status" AS ENUM('submitted', 'operator_review', 'accepted', 'rejected');--> statement-breakpoint
CREATE TYPE "public"."body_war_suggested_track_status" AS ENUM('needs_evidence', 'evidence_submitted', 'operator_review', 'source_backed', 'retired');--> statement-breakpoint
CREATE TABLE "body_war_activity_evidence_candidates" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"suggested_track_id" uuid NOT NULL,
	"principal_id" uuid NOT NULL,
	"provider" varchar(64) DEFAULT 'strava' NOT NULL,
	"provider_activity_id" varchar(255) NOT NULL,
	"redacted_summary" jsonb NOT NULL,
	"consent_text" text NOT NULL,
	"consented_at" timestamp NOT NULL,
	"status" "body_war_activity_evidence_candidate_status" DEFAULT 'submitted' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "body_war_suggested_tracks" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"slug" varchar(140) NOT NULL,
	"name" varchar(255) NOT NULL,
	"place_label" varchar(255) NOT NULL,
	"city" varchar(120) NOT NULL,
	"country" varchar(2) DEFAULT 'BR' NOT NULL,
	"distance_hint_meters" integer,
	"status" "body_war_suggested_track_status" DEFAULT 'needs_evidence' NOT NULL,
	"geometry_authority" varchar(64) DEFAULT 'needs_evidence' NOT NULL,
	"suggested_by_principal_id" uuid,
	"public_note" text DEFAULT '' NOT NULL,
	"created_at" timestamp DEFAULT now() NOT NULL,
	"updated_at" timestamp DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX "body_war_suggested_tracks_unique_slug" ON "body_war_suggested_tracks" USING btree ("slug");