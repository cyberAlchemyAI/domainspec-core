export {
  DEFAULT_AUTH_CONFIG,
  mergeAuthConfig,
  type AuthConfig,
} from "./auth-config.js";
export { noopAuthTelemetry, type AuthTelemetry } from "./auth-telemetry.js";
export { fixedClock, systemClock, type Clock } from "./clock.js";
export {
  randomUuidGenerator,
  type IdGenerator,
} from "./id-generator.js";
export {
  createPbkdf2PasswordService,
  createPlainTextPasswordServiceForTests,
  type PasswordService,
  type Pbkdf2PasswordServiceOptions,
} from "./password-service.js";
export {
  createHmacTokenCodec,
  TokenCodecError,
  type SignTokenOptions,
  type TokenClaims,
  type TokenCodec,
  type VerifyTokenOptions,
} from "./token-codec.js";
