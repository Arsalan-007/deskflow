import { NextResponse } from "next/server";
import { dispatchDigestWorkflow } from "../../../lib/github";

// Reached only if middleware's session-cookie check already passed.
export async function POST() {
  try {
    await dispatchDigestWorkflow();
    return NextResponse.json({ ok: true });
  } catch (e) {
    return NextResponse.json({ ok: false, error: (e as Error).message }, { status: 502 });
  }
}
