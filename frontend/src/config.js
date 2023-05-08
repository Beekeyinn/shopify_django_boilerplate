import createApp from "@shopify/app-bridge";
import { authenticatedFetch } from "@shopify/app-bridge/utilities";

export const config = {
  apiKey: process.env.SHOPIFY_API_KEY,
  host: new URLSearchParams(location.search).get("host"),
  forceRedirect: true,
};

export const shopifyApp = createApp(config);

export const shopifyAuthenticatedFetch = authenticatedFetch(shopifyApp);
