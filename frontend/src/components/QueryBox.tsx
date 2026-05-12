"use client";

import { useState } from "react";
import { useMe, useQueryMutation, useWorkspaces } from "@/hooks/useAdminData";
import { Button } from "@/components/ui/Button";
import { BrutalCard } from "@/components/ui/BrutalCard";
import { EmptyState } from "@/components/ui/EmptyState";

export function QueryBox() {
  const [text, setText] = useState("");
  const mutation = useQueryMutation();
  const workspaces = useWorkspaces();
  const me = useMe();
  const workspaceId = workspaces.data?.items[0]?.workspace_id;
  const result = mutation.data;
  return (
    <BrutalCard>
      {!workspaceId || !me.data ? <EmptyState title="No query workspace" detail="Sign in with an authorized workspace membership before asking AccordIQ." /> : (
        <>
          <textarea className="min-h-28 w-full border-2 border-ink bg-paper p-3 font-semibold outline-none" placeholder="Ask about captured workspace context..." value={text} onChange={(event) => setText(event.target.value)} />
          <Button className="mt-3 bg-amber" onClick={() => mutation.mutate({ workspace_id: workspaceId, user_id: me.data.id, text })} disabled={!text.trim()}>Ask AccordIQ</Button>
          <div className="mt-5">
            {!result ? <EmptyState title="No answer yet" detail="Ask a grounded recall question to inspect citations." /> : (
              <div className="border-2 border-ink bg-white p-4">
                <p className="font-display text-xl font-black">{result.answer}</p>
                <div className="mt-3 grid gap-2">
                  {result.citations.length === 0 ? <p className="font-bold">No citations returned.</p> : result.citations.map((citation, index) => <a className="border-2 border-ink bg-cream p-2 font-bold" href={citation.url || undefined} key={`${citation.title}-${index}`}>{citation.title} - {citation.preview}</a>)}
                </div>
              </div>
            )}
          </div>
        </>
      )}
    </BrutalCard>
  );
}
