const durable = process.env.BODY_WAR_IDENTITY_MODE === 'oidc-durable';
export const OIDC_POLICY = Object.freeze({ issuer: 'https://localhost:18443/realms/auth-https', origin: durable ? 'https://body-war-durable.localhost:16443' : 'https://body-war.localhost:14443', client: durable ? 'body-war-durable-browser' : 'body-war-v2-browser', audience: durable ? 'body-war-durable-api' : 'body-war-v2-api', idle: 900, max: 28800 });
const wall = () => Math.floor(Date.now() / 1000);
export function authenticationTime(authTime, issued, fresh, time = wall()) {
    if (!Number.isSafeInteger(authTime) || Number(authTime) > time || Number(authTime) < 0 || (fresh && Number(authTime) < issued) || time - Number(authTime) > OIDC_POLICY.max)
        throw Error('Authentication freshness rejected');
}
export function stateStatus(s, time) { if (!s || s.status !== 'active')
    return 'invalid_session'; if (time >= s.absolute || time >= s.last + OIDC_POLICY.idle)
    return 'session_expired'; return 'active'; }
//# sourceMappingURL=oidc-policy.js.map