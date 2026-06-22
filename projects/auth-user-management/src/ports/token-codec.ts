import { createHmac, timingSafeEqual } from "node:crypto";

export type TokenClaims = {
  sid?: unknown;
  jti?: unknown;
  iat?: number;
  exp?: number;
  [key: string]: unknown;
};

export type SignTokenOptions = {
  expiresInSeconds: number;
  issuedAt?: Date;
};

export type VerifyTokenOptions = {
  ignoreExpiration?: boolean;
  now?: Date;
};

export type TokenCodec = {
  sign(payload: TokenClaims, options: SignTokenOptions): Promise<string>;
  verify(token: string, options?: VerifyTokenOptions): Promise<TokenClaims>;
};

export class TokenCodecError extends Error {
  constructor(
    public readonly code: "INVALID_TOKEN" | "TOKEN_EXPIRED",
    message: string,
  ) {
    super(message);
    this.name = "TokenCodecError";
  }
}

export function createHmacTokenCodec(secret: string): TokenCodec {
  if (secret.trim().length === 0) {
    throw new Error("Token codec secret must not be empty");
  }

  return {
    async sign(payload, options) {
      const issuedAtSeconds = Math.floor(
        (options.issuedAt ?? new Date()).getTime() / 1000,
      );
      const claims: TokenClaims = {
        ...payload,
        iat: payload.iat ?? issuedAtSeconds,
        exp: payload.exp ?? issuedAtSeconds + options.expiresInSeconds,
      };
      const encodedClaims = encodeBase64Url(JSON.stringify(claims));
      const signature = sign(encodedClaims, secret);
      return `${encodedClaims}.${signature}`;
    },

    async verify(token, options = {}) {
      const [encodedClaims, signature, extra] = token.split(".");
      if (!encodedClaims || !signature || extra !== undefined) {
        throw new TokenCodecError("INVALID_TOKEN", "Malformed token");
      }

      const expectedSignature = sign(encodedClaims, secret);
      if (!safeEqual(signature, expectedSignature)) {
        throw new TokenCodecError("INVALID_TOKEN", "Invalid token signature");
      }

      let claims: TokenClaims;
      try {
        claims = JSON.parse(
          Buffer.from(encodedClaims, "base64url").toString("utf8"),
        ) as TokenClaims;
      } catch {
        throw new TokenCodecError("INVALID_TOKEN", "Invalid token payload");
      }

      const nowSeconds = Math.floor((options.now ?? new Date()).getTime() / 1000);
      if (
        options.ignoreExpiration !== true &&
        typeof claims.exp === "number" &&
        nowSeconds >= claims.exp
      ) {
        throw new TokenCodecError("TOKEN_EXPIRED", "Token expired");
      }

      return claims;
    },
  };
}

function sign(payload: string, secret: string): string {
  return createHmac("sha256", secret).update(payload).digest("base64url");
}

function safeEqual(left: string, right: string): boolean {
  const leftBuffer = Buffer.from(left);
  const rightBuffer = Buffer.from(right);
  return (
    leftBuffer.length === rightBuffer.length &&
    timingSafeEqual(leftBuffer, rightBuffer)
  );
}

function encodeBase64Url(value: string): string {
  return Buffer.from(value, "utf8").toString("base64url");
}
