import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./assets/css/main.css";
import { store } from "./store";

const Homepage = React.lazy(() => import("./pages/main/Main"));
const App = React.lazy(() => import("./App"));
const components = {
  app: App,
};

const componentMapper = (id, Component) => {
  try {
    const rootElement = ReactDOM.createRoot(document.getElementById(id));
    rootElement.render(
      <React.StrictMode>
        <Provider store={store}>
          <ToastContainer />
          <Component />
        </Provider>
      </React.StrictMode>
    );
  } catch (e) {}
};

if (process.env.DEVELOPMENT === "true") {
  const rootElement = ReactDOM.createRoot(document.getElementById("root"));
  rootElement.render(
    <Provider store={store}>
      <ToastContainer />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Homepage />} />
        </Routes>
      </BrowserRouter>
    </Provider>
  );
} else {
  for (let key in components) {
    componentMapper(key, components[key]);
  }
}
