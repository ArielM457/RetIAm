type RuntimeConfig = {
  apiBaseUrl?: string;
  supabaseUrl?: string;
  supabaseAnonKey?: string;
};

declare global {
  interface Window {
    __RETAIM_CONFIG__?: RuntimeConfig;
  }
}

function assertConfigValue(value: string | undefined, label: string): string {
  if (!value) {
    throw new Error(`Missing runtime config value: ${label}`);
  }

  return value;
}

export const runtimeConfig = {
  get apiBaseUrl(): string {
    return assertConfigValue(window.__RETAIM_CONFIG__?.apiBaseUrl, 'apiBaseUrl');
  },
  get supabaseUrl(): string {
    return assertConfigValue(window.__RETAIM_CONFIG__?.supabaseUrl, 'supabaseUrl');
  },
  get supabaseAnonKey(): string {
    return assertConfigValue(window.__RETAIM_CONFIG__?.supabaseAnonKey, 'supabaseAnonKey');
  },
};
