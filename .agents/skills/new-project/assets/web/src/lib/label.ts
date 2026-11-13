export function serviceLabel(name: string): string {
  const trimmed = name.trim();
  if (!trimmed) {
    throw new Error("service name is empty");
  }
  return trimmed;
}
