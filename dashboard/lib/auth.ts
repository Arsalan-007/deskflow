/**
 * Signed session cookie, built on Web Crypto (not node:crypto) so the same
 * code runs in both the Edge middleware and Node route handlers.
 */

const SESSION_COOKIE = "deskflow_session";
const SESSION_TTL_MS = 12 * 60 * 60 * 1000; // 12h

function base64url(bytes: ArrayBuffer | Uint8Array): string {
  const u8 = bytes instanceof Uint8Array ? bytes : new Uint8Array(bytes);
  return Buffer.from(u8).toString("base64url");
}

async function hmac(secret: string, data: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(data));
  return base64url(sig);
}

/** Constant-time string compare (equal-length base64url signatures). */
function timingSafeStringEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

export async function createSessionCookieValue(secret: string): Promise<string> {
  const payload = base64url(new TextEncoder().encode(JSON.stringify({ exp: Date.now() + SESSION_TTL_MS })));
  const sig = await hmac(secret, payload);
  return `${payload}.${sig}`;
}

export async function verifySessionCookieValue(value: string | undefined, secret: string): Promise<boolean> {
  if (!value) return false;
  const [payload, sig] = value.split(".");
  if (!payload || !sig) return false;
  const expectedSig = await hmac(secret, payload);
  if (!timingSafeStringEqual(sig, expectedSig)) return false;
  try {
    const { exp } = JSON.parse(Buffer.from(payload, "base64url").toString("utf8"));
    return typeof exp === "number" && Date.now() < exp;
  } catch {
    return false;
  }
}

export { SESSION_COOKIE, SESSION_TTL_MS };
