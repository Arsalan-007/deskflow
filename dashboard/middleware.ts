import { NextRequest, NextResponse } from "next/server";
import { SESSION_COOKIE, verifySessionCookieValue } from "./lib/auth";

export async function middleware(req: NextRequest) {
  const cookie = req.cookies.get(SESSION_COOKIE)?.value;
  const secret = process.env.COOKIE_SECRET;
  if (!secret) {
    // Fail closed: a missing secret must never silently open the gate.
    return new NextResponse("DeskFlow dashboard misconfigured: COOKIE_SECRET not set", { status: 500 });
  }

  const authed = await verifySessionCookieValue(cookie, secret);
  if (authed) return NextResponse.next();

  if (req.nextUrl.pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }
  const loginUrl = new URL("/login", req.url);
  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: ["/((?!login|api/login|_next/static|_next/image|favicon.ico).*)"],
};
