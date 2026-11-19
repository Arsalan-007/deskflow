import { createHash, timingSafeEqual } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";
import { SESSION_COOKIE, SESSION_TTL_MS, createSessionCookieValue } from "../../../lib/auth";

// Hash both sides to a fixed-length digest first: timingSafeEqual throws on
// unequal-length buffers, and raw passphrases are variable-length.
function passphraseMatches(submitted: string, expected: string): boolean {
  const a = createHash("sha256").update(submitted).digest();
  const b = createHash("sha256").update(expected).digest();
  return timingSafeEqual(a, b);
}

export async function POST(req: NextRequest) {
  const secret = process.env.COOKIE_SECRET;
  const accessCode = process.env.DASHBOARD_ACCESS_CODE;
  if (!secret || !accessCode) {
    return NextResponse.json({ error: "dashboard misconfigured" }, { status: 500 });
  }

  const { passphrase } = await req.json().catch(() => ({ passphrase: "" }));
  if (typeof passphrase !== "string" || !passphraseMatches(passphrase, accessCode)) {
    return NextResponse.json({ error: "incorrect passphrase" }, { status: 401 });
  }

  const res = NextResponse.json({ ok: true });
  res.cookies.set(SESSION_COOKIE, await createSessionCookieValue(secret), {
    httpOnly: true,
    secure: true,
    sameSite: "strict",
    maxAge: SESSION_TTL_MS / 1000,
    path: "/",
  });
  return res;
}
