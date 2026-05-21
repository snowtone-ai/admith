function baseUrl(): string {
  if (typeof window === "undefined") return process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://backend:8000";
  return process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
}

export function apiKey(): string {
  if (typeof window === "undefined") return "test-key";
  return localStorage.getItem("admith_api_key") ?? "test-key";
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${baseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey()}`,
      ...(init.headers ?? {})
    },
    cache: "no-store"
  });
  if (!response.ok) throw new Error(`API ${response.status}`);
  return response.json() as Promise<T>;
}
