"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect } from "react";
import { setAccessToken } from "@/lib/apiClient";

function CallbackContent() {
  const router = useRouter();
  const params = useSearchParams();
  useEffect(() => {
    const token = params.get("token");
    const error = params.get("error");
    if (token) {
      setAccessToken(token);
      router.replace("/");
      return;
    }
    router.replace(`/login${error ? `?error=${encodeURIComponent(error)}` : ""}`);
  }, [params, router]);
  return <main className="grid min-h-screen place-items-center bg-paper font-display text-2xl font-black">Signing you in...</main>;
}

export default function AuthCallbackPage() {
  return (
    <Suspense fallback={<main className="grid min-h-screen place-items-center bg-paper font-display text-2xl font-black">Signing you in...</main>}>
      <CallbackContent />
    </Suspense>
  );
}
