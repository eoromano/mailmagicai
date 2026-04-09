import { createMockOutlookAdapter, createOutlookAdapter } from "../adapters";
import { createApiClient } from "./apiClient";
import { createMockClient } from "./mockClient";

const appMode = import.meta.env.VITE_APP_MODE ?? "mock";
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";
const messageSource = import.meta.env.VITE_MESSAGE_SOURCE ?? "mock";

export type DataMode = "mock" | "api";
export type AdapterMode = "mock" | "outlook";

export const defaultMockMode = appMode !== "api";

export function resolveDataMode(mockMode: boolean): DataMode {
  return mockMode ? "mock" : "api";
}

export function resolveAdapterMode(mockMode: boolean): AdapterMode {
  return mockMode ? "mock" : messageSource === "outlook" ? "outlook" : "mock";
}

export function createThreadSenseClient(mode: DataMode) {
  return mode === "api" ? createApiClient({ baseUrl: apiBaseUrl }) : createMockClient();
}

export function createOutlookDataAdapter(mode: AdapterMode) {
  return mode === "outlook" ? createOutlookAdapter() : createMockOutlookAdapter();
}
