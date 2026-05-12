"use client";

import { useState } from "react";
import { useQueryMutation } from "@/hooks/useAdminData";
import { Button } from "@/components/ui/Button";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { EmptyState } from "@/components/ui/EmptyState";

export function QueryBox() {
  const [text, setText] = useState("what did we decide about onboarding?");
  const mutation = useQueryMutation();
  const result = mutation.data;
  return (
    <BrutalCard>
      <textarea className="min-h-28 w-full border-2 border-ink bg-paper p-3 font-semibold outline-none" value={text} onChange={(event) => setText(event.target.value)} />
      <Button className="mt-3 bg-amber" onClick={() => mutation.mutate({ workspace_id: "demo-workspace", user_id: "demo-user", text })}>Ask AccordIQ</Button>
      <div className="mt-5">
        {!result ? <EmptyState title="No answer yet" detail="Ask a grounded recall question to inspect citations." /> : (
          <div className="border-2 border-ink bg-white p-4">
            <p className="font-display text-xl font-black">{result.answer}</p>
            <div className="mt-3 grid gap-2">
              {result.citations.map((citation) => <a className="border-2 border-ink bg-cream p-2 font-bold" href={citation.url} key={citation.url}>{citation.title} - {citation.preview}</a>)}
            </div>
          </div>
        )}
      </div>
    </BrutalCard>
  );
}
