"use client";

import { LogIn } from "lucide-react";
import { authStartUrl } from "@/lib/apiClient";

export default function LoginPage() {
  return (
    <main className="grid min-h-screen place-items-center bg-paper p-4">
      <section className="w-full max-w-xl border-2 border-ink bg-white p-8 shadow-brutal">
        <div className="grid size-14 place-items-center border-2 border-ink bg-amber font-display text-2xl font-black shadow-brutalSm">AIQ</div>
        <h1 className="mt-6 font-display text-5xl font-black">AccordIQ</h1>
        <p className="mt-3 text-lg font-semibold">Sign in with an invited Google account to manage workspace memory, review entities, and run grounded queries.</p>
        <a className="mt-6 inline-flex items-center gap-3 border-2 border-ink bg-ink px-5 py-3 font-display font-black text-white shadow-brutalSm hover:bg-blue" href={authStartUrl}>
          <LogIn size={20} />
          Continue with Google
        </a>
      </section>
    </main>
  );
}
