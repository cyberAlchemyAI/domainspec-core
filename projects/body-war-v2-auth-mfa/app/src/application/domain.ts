// Generated lifecycle and explicit redaction projections.
export const configuration = {
  "HistoricalActivityPolicy": {
    "timeoutMs": 10000,
    "maxResponseBytes": 1048576,
    "identityFields": [
      "id",
      "athlete.id"
    ],
    "persistRawDetail": false
  },
  "TrackDefaults": {
    "seed": {
      "slug": "volta-do-taquaral",
      "name": "Volta do Taquaral",
      "placeLabel": "Parque Portugal / Lagoa do Taquaral",
      "city": "Campinas",
      "country": "BR",
      "distanceHintMeters": 6400,
      "publicNote": "Sugestao inicial para reunir evidencias antes de qualquer geometria source-backed."
    }
  },
  "EvidencePolicy": {
    "consentRequired": true,
    "duplicateScope": [
      "principalId",
      "suggestedTrackId",
      "providerActivityId"
    ],
    "retention": "until deletion or consent revocation; repository disposal removes candidate and resets empty track",
    "providerRevocation": "disconnect and erase stored provider ciphertext",
    "authority": {
      "activity_summary": "redacted_candidate",
      "route_geometry": "not_claimed",
      "scoring": "not_claimed"
    }
  },
  "RuntimeConfiguration": {
    "local": {
      "host": "127.0.0.1",
      "port": 5184,
      "authBackend": "memory",
      "fakeStrava": true
    },
    "identity": {
      "profiles": [
        "strava-pilot",
        "oidc",
        "oidc-durable"
      ],
      "durable": {
        "origin": "https://body-war-durable.localhost:16443",
        "client": "body-war-durable-browser",
        "audience": "body-war-durable-api",
        "store": "@auth-foundation/session-core",
        "backend": "postgres",
        "namespace": "body-war"
      },
      "oidcIssuer": "https://localhost:18443/realms/auth-https",
      "oidcOrigin": "https://body-war.localhost:14443",
      "client": "body-war-v2-browser",
      "audience": "body-war-v2-api",
      "idleSeconds": 900,
      "maximumSeconds": 28800
    },
    "secrets": [
      "BODY_WAR_DURABLE_KEY",
      "BODY_WAR_OIDC_CLIENT_SECRET",
      "BODY_WAR_SESSION_SECRET",
      "BODY_WAR_TOKEN_PROTECTION_SECRET",
      "STRAVA_CLIENT_SECRET",
      "BODY_WAR_DATABASE_URL"
    ],
    "provider": [
      "STRAVA_CLIENT_ID",
      "STRAVA_REDIRECT_URI"
    ],
    "session": {
      "sameSite": "Lax",
      "httpOnly": true,
      "csrfOriginRequiredForMutation": true
    },
    "hosting": "local Node HTTP; no RWO deployment binding",
    "recovery": "repository disposal idempotency and migration checksum ledger; no general durable outbox/canary claim"
  },
  "UiConfiguration": {
    "consentText": "Autorizo o TROQAR a guardar somente o resumo redigido desta atividade como candidata de evidencia para a rota sugerida.",
    "brand": "TROQAR",
    "provider": "Strava",
    "errors": {
      "security_action_finished": "A acao de seguranca terminou. Entre novamente para continuar.",
      "consent_required": "Confirme o consentimento antes de enviar a candidata.",
      "invalid_suggested_track": "Preencha nome, lugar, cidade e uma distancia positiva quando informada.",
      "suggested_track_not_found": "Esta rota sugerida nao esta mais disponivel.",
      "track_geometry_missing": "Geometria da rota ainda nao foi confirmada para esta evidencia."
    }
  },
  "CriticalRequirements": {
    "requirements": [
      {
        "case": "runner_isolation",
        "id": "SEC_ISOLATION",
        "formal": "Runner-scoped detail returns no other runner evidence and profile resolves to the authenticated principal.",
        "evidence": "evidence/critical-security.json",
        "test": "scripts/critical-security.mjs"
      },
      {
        "case": "permissions",
        "id": "SEC_PERMISSION",
        "formal": "Anonymous access returns 401 and an authenticated principal without the read grant receives 403.",
        "evidence": "evidence/critical-security.json",
        "test": "scripts/critical-security.mjs"
      },
      {
        "case": "oauth_replay",
        "id": "SEC_OAUTH_REPLAY",
        "formal": "A consumed OAuth callback cannot mint a second browser session.",
        "evidence": "evidence/critical-security.json",
        "test": "scripts/critical-security.mjs"
      },
      {
        "case": "csrf_origin",
        "id": "SEC_CSRF",
        "formal": "Missing CSRF and an untrusted origin reject a valid-session write.",
        "evidence": "evidence/critical-security.json",
        "test": "scripts/critical-security.mjs"
      },
      {
        "case": "request_validation",
        "id": "SEC_REQUEST",
        "formal": "Malformed, unknown-field, wrong-type and oversized JSON requests are rejected before persistence.",
        "evidence": "evidence/critical-security.json",
        "test": "scripts/critical-security.mjs"
      },
      {
        "case": "consent_revocation",
        "id": "SEC_REVOCATION",
        "formal": "Internal consent disposition erases the exact candidate, resets the empty track and is idempotent.",
        "evidence": "evidence/critical-security.json",
        "test": "scripts/critical-security.mjs"
      },
      {
        "case": "oauth_concurrency",
        "id": "DB_OAUTH",
        "formal": "Twelve concurrent PostgreSQL consumers return exactly one OAuth state; expiry at the boundary is rejected.",
        "evidence": "evidence/critical-postgres.json",
        "test": "app/e2e/critical-integrity.e2e.ts"
      },
      {
        "case": "evidence_concurrency",
        "id": "DB_DUPLICATE",
        "formal": "Twelve concurrent identical attachments create exactly one row; uniqueness includes runner identity.",
        "evidence": "evidence/critical-postgres.json",
        "test": "app/e2e/critical-integrity.e2e.ts"
      },
      {
        "case": "atomic_rollback",
        "id": "DB_ATOMIC",
        "formal": "Failure between evidence insertion and track update rolls both back and permits one successful retry.",
        "evidence": "evidence/critical-postgres.json",
        "test": "app/e2e/critical-integrity.e2e.ts"
      },
      {
        "case": "concurrent_disposition",
        "id": "DB_DISPOSITION",
        "formal": "Concurrent disposition and replacement preserve the new candidate and consistent track state.",
        "evidence": "evidence/critical-postgres.json",
        "test": "app/e2e/critical-integrity.e2e.ts"
      },
      {
        "case": "persistence_reopen",
        "id": "DB_PERSISTENCE",
        "formal": "A fresh reader process sees committed evidence and track state after all writer connections close.",
        "evidence": "evidence/critical-postgres.json",
        "test": "app/e2e/critical-integrity.e2e.ts"
      }
    ]
  }
} as const;
export const enumValues = {
  "StravaProvider": [
    "strava"
  ],
  "ProviderStatus": [
    "linked",
    "disconnected"
  ],
  "SuggestedTrackStatus": [
    "needs_evidence",
    "evidence_submitted",
    "operator_review",
    "source_backed",
    "retired"
  ],
  "NoClaim": [
    "not_claimed"
  ],
  "ActivityEvidenceCandidateStatus": [
    "submitted",
    "operator_review",
    "accepted",
    "rejected"
  ]
} as const;
const lifecycles: Record<string,{initial:string;transitions:string[][]}> = {
  "TrackEvidenceLifecycle": {
    "initial": "needs_evidence",
    "transitions": [
      [
        "needs_evidence",
        "attach",
        "evidence_submitted"
      ],
      [
        "evidence_submitted",
        "attach",
        "evidence_submitted"
      ],
      [
        "operator_review",
        "attach",
        "operator_review"
      ],
      [
        "source_backed",
        "attach",
        "source_backed"
      ],
      [
        "retired",
        "attach",
        "retired"
      ],
      [
        "needs_evidence",
        "last-evidence-removed",
        "needs_evidence"
      ],
      [
        "evidence_submitted",
        "last-evidence-removed",
        "needs_evidence"
      ],
      [
        "operator_review",
        "last-evidence-removed",
        "needs_evidence"
      ],
      [
        "source_backed",
        "last-evidence-removed",
        "needs_evidence"
      ],
      [
        "retired",
        "last-evidence-removed",
        "needs_evidence"
      ]
    ]
  }
};
const projections: Record<string,Record<string,string[]>> = {
  "RedactedActivity": {
    "id": [
      "id"
    ],
    "name": [
      "name"
    ],
    "sport_type": [
      "sport_type",
      "type",
      "literal:Run"
    ],
    "type": [
      "type",
      "sport_type",
      "literal:Run"
    ],
    "distance": [
      "distance"
    ],
    "moving_time": [
      "moving_time"
    ],
    "average_speed": [
      "average_speed"
    ],
    "start_date": [
      "start_date"
    ]
  }
};
export function transition(id:string,state:string,event:string):string {const lifecycle=lifecycles[id];if(!lifecycle)throw Error('UNKNOWN_LIFECYCLE');const t=lifecycle.transitions.find(t=>t[0]===state&&t[1]===event);if(!t)throw Error('INVALID_TRANSITION');return t[2]!;}
export function project(id:string,input:Readonly<Record<string,unknown>>):Record<string,unknown>{const fields=projections[id];if(!fields)throw Error('UNKNOWN_PROJECTION');const result:Record<string,unknown>={};for(const [key,refs]of Object.entries(fields)){for(const ref of refs){const descriptor=Object.getOwnPropertyDescriptor(input,ref);const value=ref.startsWith('literal:')?ref.slice(8):descriptor&&'value' in descriptor?descriptor.value:undefined;if(value!==null&&value!==undefined){result[key]=value;break;}}}return result;}
