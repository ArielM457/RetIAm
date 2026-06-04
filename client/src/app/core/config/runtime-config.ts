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
    throw new Error(
      `Missing runtime config value: ${label}. Completa client/public/runtime-config.js antes de iniciar el frontend.`,
    );
  }

  const normalizedValue = value.trim();
  const isPlaceholderValue =
    normalizedValue.includes('YOUR_PROJECT') ||
    normalizedValue.includes('YOUR_SUPABASE_ANON_KEY') ||
    normalizedValue.includes('your_project') ||
    normalizedValue.includes('your_supabase_anon_key');

  if (isPlaceholderValue) {
    throw new Error(
      `Invalid runtime config value: ${label}. client/public/runtime-config.js todavia tiene placeholders y debe apuntar a tu proyecto real de Supabase.`,
    );
  }

  return normalizedValue;
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
