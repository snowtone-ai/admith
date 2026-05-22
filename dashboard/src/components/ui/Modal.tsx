"use client";

import { useEffect, useRef } from "react";
import { Button } from "./button";

interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
}

export function Modal({ open, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const el = dialogRef.current;
    if (!el) return;
    if (open && !el.open) el.showModal();
    if (!open && el.open) el.close();
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      onClose={onClose}
      className={[
        "fixed inset-0 z-50 m-auto",
        "max-w-lg w-full rounded-xl bg-surface-2 p-8 text-ink",
        "backdrop:bg-[var(--color-overlay)] backdrop:backdrop-blur-sm",
        "animate-[modal-in_250ms_cubic-bezier(0.16,1,0.3,1)]",
      ].join(" ")}
      style={{
        border: "none",
      }}
      onClick={(e) => { if (e.target === dialogRef.current) onClose(); }}
    >
      <div className="flex items-start justify-between">
        {title ? <h2 className="font-display text-lg font-semibold">{title}</h2> : null}
        <Button variant="ghost" size="sm" onClick={onClose} aria-label="閉じる">
          <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </Button>
      </div>
      <div className="mt-4">{children}</div>
    </dialog>
  );
}
