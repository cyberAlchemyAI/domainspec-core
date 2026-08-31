import { defaultValueCtx, Editor, rootAttrsCtx, rootCtx } from "@milkdown/core";
import { history } from "@milkdown/plugin-history";
import { listener, listenerCtx } from "@milkdown/plugin-listener";
import { commonmark } from "@milkdown/preset-commonmark";
import { useEffect, useRef, useState } from "react";

interface MilkdownEditorProps {
  initialMarkdown: string;
  onMarkdownChange: (markdown: string) => void;
  onSettlingChange: (settling: boolean) => void;
  describedBy: string;
}

export function MilkdownEditor({ initialMarkdown, onMarkdownChange, onSettlingChange, describedBy }: MilkdownEditorProps) {
  const rootRef = useRef<HTMLDivElement>(null);
  const onChangeRef = useRef(onMarkdownChange);
  const onSettlingRef = useRef(onSettlingChange);
  const [status, setStatus] = useState<"loading" | "ready" | "failed">("loading");

  onChangeRef.current = onMarkdownChange;
  onSettlingRef.current = onSettlingChange;

  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    let disposed = false;
    const editor = Editor.make()
      .config((ctx) => {
        ctx.set(rootCtx, root);
        ctx.set(defaultValueCtx, initialMarkdown);
        ctx.set(rootAttrsCtx, {
          "aria-label": "Essay Markdown editor",
          "aria-describedby": describedBy,
          "data-testid": "milkdown-editor",
        });
        ctx.get(listenerCtx).markdownUpdated((_ctx, markdown, previousMarkdown) => {
          if (markdown !== previousMarkdown) onChangeRef.current(markdown);
          onSettlingRef.current(false);
        });
      })
      .use(commonmark)
      .use(history)
      .use(listener);

    const markSettling = () => onSettlingRef.current(true);
    root.addEventListener("input", markSettling);
    void editor
      .create()
      .then(() => {
        if (!disposed) setStatus("ready");
      })
      .catch(() => {
        if (!disposed) setStatus("failed");
      });

    return () => {
      disposed = true;
      root.removeEventListener("input", markSettling);
      onSettlingRef.current(false);
      void editor.destroy();
    };
    // A deliberate remount is controlled by the parent key after an accepted revision.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="editor-adapter" data-editor-status={status}>
      {status === "loading" && <p className="editor-status">Preparing the writing surface…</p>}
      {status === "failed" && <p className="editor-status error">The editor could not start. Reload the local studio.</p>}
      <div ref={rootRef} />
    </div>
  );
}
