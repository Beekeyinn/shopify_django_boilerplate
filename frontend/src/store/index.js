import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";
import stableAPI from "./api";
import newSlice from "./slice";

const store = configureStore({
  reducer: {
    [stableAPI.reducerPath]: stableAPI.reducer,
    slice: newSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(stableAPI.middleware),
});

export { store };
export const newAction = newSlice.actions;
export const { useIdentityUserQuery } = stableAPI;

export * from "./actions";
