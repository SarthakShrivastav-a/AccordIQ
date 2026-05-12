"use client";

import { usePathname, useRouter } from "next/navigation";
import { ReactNode, useEffect } from "react";
import { getAccessToken } from "@/lib/apiClient";

const publicPaths = ["/login", "/auth/callback"];

export function AuthGate({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  useEffect(() => {
    if (!publicPaths.includes(pathname) && !getAccessToken()) router.replace("/login");
  }, [pathname, router]);
  return <>{children}</>;
}
