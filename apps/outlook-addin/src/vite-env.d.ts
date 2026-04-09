/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_MODE?: "mock" | "api";
  readonly VITE_API_BASE_URL?: string;
  readonly VITE_MESSAGE_SOURCE?: "mock" | "outlook";
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
