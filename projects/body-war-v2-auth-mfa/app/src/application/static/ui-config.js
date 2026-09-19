// Generated API paths and UI state contracts.
export const config={
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
};
export const views=[
  {
    "id": "LoginView",
    "selector": "#auth-login",
    "visibility": "anonymous",
    "operations": [
      "StartStrava",
      "CompleteStrava",
      "StartOidc",
      "CompleteOidc",
      "LinkStrava"
    ]
  },
  {
    "id": "RunnerHomeView",
    "selector": "#runner-home",
    "visibility": "connected",
    "operations": [
      "ReadProfile",
      "ListActivities",
      "ListTracks",
      "CreateTrack",
      "ReadTrack",
      "AttachEvidence",
      "WithdrawEvidence"
    ]
  },
  {
    "id": "LogoutView",
    "selector": "#logout",
    "visibility": "connected",
    "operations": [
      "Logout"
    ]
  },
  {
    "id": "ProfileLinkView",
    "selector": "#profile-link",
    "visibility": "connected",
    "operations": [
      "ReadProfile"
    ]
  },
  {
    "id": "TopConnectView",
    "selector": "#connect-top",
    "visibility": "never",
    "operations": [
      "StartStrava"
    ]
  },
  {
    "id": "SecurityView",
    "selector": "#security-link",
    "visibility": "never",
    "operations": [
      "ReadSecurity",
      "ChangeSecurity"
    ]
  }
];
const routes={
  "ListActivities": {
    "method": "GET",
    "path": "/api/activities"
  },
  "Logout": {
    "method": "POST",
    "path": "/api/auth/logout"
  },
  "CompleteOidc": {
    "method": "GET",
    "path": "/api/auth/oidc/callback"
  },
  "StartOidc": {
    "method": "GET",
    "path": "/api/auth/oidc/start"
  },
  "ReadSecurity": {
    "method": "GET",
    "path": "/api/auth/security"
  },
  "ChangeSecurity": {
    "method": "POST",
    "path": "/api/auth/security"
  },
  "CompleteStrava": {
    "method": "GET",
    "path": "/api/auth/strava/callback"
  },
  "LinkStrava": {
    "method": "POST",
    "path": "/api/auth/strava/link"
  },
  "StartStrava": {
    "method": "GET",
    "path": "/api/auth/strava/start"
  },
  "ReadProfile": {
    "method": "GET",
    "path": "/api/profile"
  },
  "ReadStatus": {
    "method": "GET",
    "path": "/api/status"
  },
  "ListTracks": {
    "method": "GET",
    "path": "/api/suggested-tracks"
  },
  "CreateTrack": {
    "method": "POST",
    "path": "/api/suggested-tracks"
  },
  "WithdrawEvidence": {
    "method": "POST",
    "path": "/api/evidence-candidates/:id/withdraw"
  },
  "ReadTrack": {
    "method": "GET",
    "path": "/api/suggested-tracks/:idOrSlug"
  },
  "AttachEvidence": {
    "method": "POST",
    "path": "/api/suggested-tracks/:idOrSlug/evidence-candidates"
  }
};
export function apiPath(operation,parameters={}){const route=routes[operation];if(!route)throw Error('UNKNOWN_OPERATION');return route.path.replace(/:([a-z][A-Za-z0-9_]*)/g,(_,key)=>{if(typeof parameters[key]!=='string'||!parameters[key])throw Error('MISSING_PATH_PARAMETER');return encodeURIComponent(parameters[key]);});}
export function applyViews(document,connected){for(const view of views){const element=document.querySelector(view.selector);if(!element)throw Error('MISSING_VIEW:'+view.id);const show=view.visibility==='always'||view.visibility===(connected?'connected':'anonymous');element.classList.toggle('hidden',!show);}}
