import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * A utility function to merge Tailwind CSS classes.
 *
 * It combines the functionality of `clsx` and `tailwind-merge` to
 * conditionally apply and merge CSS classes without conflicts.
 *
 * @param {...ClassValue} inputs - The class values to merge.
 * @returns {string} The merged class string.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
