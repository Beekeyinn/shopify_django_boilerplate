import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import { getCsrfToken } from "../../utils";

const stableAPI = createApi({
  reducerPath: "api",
  baseQuery: fetchBaseQuery({
    baseUrl: process.env.BASE_API_URL,
    credentials: "include",
    prepareHeaders: (headers, api) => {
      headers.append("X-CSRFToken", getCsrfToken());
    },
  }),
  tagTypes: ["identity"],
  endpoints: (builder) => ({
    identityUser: builder.query({
      query: () => "identity/",
      providesTags: ["identity"],
    }),
  }),
});

export default stableAPI;
