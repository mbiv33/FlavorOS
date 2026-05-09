import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "@/lib/cn";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ children, className, ...rest }: CardProps) {
  return (
    <div
      className={cn(
        "bg-card-solid border border-line rounded-card shadow-sm2 overflow-hidden",
        className,
      )}
      {...rest}
    >
      {children}
    </div>
  );
}
