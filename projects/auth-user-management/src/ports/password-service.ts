import { pbkdf2Sync, randomBytes, timingSafeEqual } from "node:crypto";

export type PasswordService = {
  hash(secret: string): Promise<string>;
  verify(secret: string, hash: string): Promise<boolean>;
};

export type Pbkdf2PasswordServiceOptions = {
  iterations?: number;
  saltBytes?: number;
  keyLength?: number;
  digest?: string;
};

export function createPbkdf2PasswordService(
  options: Pbkdf2PasswordServiceOptions = {},
): PasswordService {
  const iterations = options.iterations ?? 120_000;
  const saltBytes = options.saltBytes ?? 16;
  const keyLength = options.keyLength ?? 32;
  const digest = options.digest ?? "sha256";

  return {
    async hash(secret) {
      const salt = randomBytes(saltBytes).toString("base64url");
      const derived = pbkdf2Sync(
        secret,
        salt,
        iterations,
        keyLength,
        digest,
      ).toString("base64url");

      return `pbkdf2:${digest}:${iterations}:${keyLength}:${salt}:${derived}`;
    },

    async verify(secret, hash) {
      const parts = hash.split(":");
      if (parts.length !== 6 || parts[0] !== "pbkdf2") {
        return false;
      }

      const [, storedDigest, storedIterations, storedKeyLength, salt, derived] =
        parts;
      if (
        !storedDigest ||
        !storedIterations ||
        !storedKeyLength ||
        !salt ||
        !derived
      ) {
        return false;
      }

      const candidate = pbkdf2Sync(
        secret,
        salt,
        Number(storedIterations),
        Number(storedKeyLength),
        storedDigest,
      );
      const expected = Buffer.from(derived, "base64url");

      return (
        candidate.length === expected.length &&
        timingSafeEqual(candidate, expected)
      );
    },
  };
}

export const createPlainTextPasswordServiceForTests = (): PasswordService => ({
  async hash(secret) {
    return `plain:${secret}`;
  },

  async verify(secret, hash) {
    return hash === `plain:${secret}`;
  },
});
