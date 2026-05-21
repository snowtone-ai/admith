function baseUrl(): string {
  if (typeof window === "undefined") return process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://backend:8000";
  return process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
}

export function apiKey(): string {
  if (typeof window === "undefined") return "";
  const match = document.cookie.match(/(?:^|;\s*)admith_api_key=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const key = apiKey();
  if (!key) throw new Error("API key is not set");
  const response = await fetch(`${baseUrl()}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${key}`,
      ...(init.headers ?? {})
    },
    cache: "no-store"
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`API ${response.status}: ${detail}`);
  }
  return response.json() as Promise<T>;
}
