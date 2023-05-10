# Shopify django boilerplate

This application integrate shopify with django utilizing shopify api. It is used to develop shopify app.

## What it covers:

- Authentication
- Session
- Django rest framework
- React as front end with routing through django (can be configured to route using react router dom too)
- Both shopify app bridge and django session can be used to play with shopify API

### Setup

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements/base.txt`

`cd frontend`

`npm install or yarn install`

- In order to run the react front end seperately

`yarn start or npm run start`

- In order to test the react integration with django template

`yarn stage or npm run stage`

- For production mode

`yarn build or npm run build`

# Environment

## Django environment

DEBUG=True
SECRET_KEY= your secret key

- SHOPIFY

SHOPIFY_APP_NAME="APP NAME"
SHOPIFY_API_KEY="APP API KEY"
SHOPIFY_API_SECRET="APP CLIENT KEY"
SHOPIFY_API_VERSION="unstable"
SHOPIFY_API_SCOPES="SCOPES FOR APP"
SHOPIFY_DOMAIN="YOUR SHOP DOMAIN"

- SHOPIFY_API_KEY and SHOPIFY_API_SECRET are provided by shopify when creating the shopify app in partner account.

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# NGROK URL FOR SHOPIFY TESTING PURPOSE

APP_URL=ngrok url for csrf trusted origin

## REACT ENVIRONMENT

BASE_API_URL= your django api based url or ngrok url till api
BASE_URL= your django base url eg localhost:8000
DEVELOPMENT=false for both staging and production mode
SHOPIFY_API_KEY= your shopify app api client key
SHOPIFY_SHOP_ORIGIN= your shopify shop or store url

- SHOPIFY_API_KEY and SHOPIFY_SHOP_ORIGIN are needed if you are using react app bridge.

# React App bridge configuration

- add following code in index js at frontend/src/index.js file

```
import { config } from "./config";
import {
  Provider as ShopifyProvider,
  Loading,
} from "@shopify/app-bridge-react";
```

- now replace componentmapper function with following code:

```
const componentMapper = (id, Component) => {
  try {
    const rootElement = ReactDOM.createRoot(document.getElementById(id));
    rootElement.render(
      <React.StrictMode>
        <Provider store={store}>
          <ShopifyProvider config={config}>
            <Loading />
            <ToastContainer />
            <Component />
          </ShopifyProvider>
        </Provider>
      </React.StrictMode>
    );
  } catch (e) {}
};
```

Also if you are using react router dom for navigation replace the following code in src/index.js

```
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
```

with this code:

```
  const rootElement = ReactDOM.createRoot(document.getElementById("root"));
  rootElement.render(
    <Provider store={store}>
    <ShopifyProvider config={config}>
      <ToastContainer />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="design" element={<Test />} />
          <Route path="homepage" element={<Homepage />} />
        </Routes>
      </BrowserRouter>
    </ShopifyProvider>
    </Provider>
  );
```
* also remove .env.staging and webpack.dev.js file form the frontend. 
* in .env.staging replace DEVELOPMENT=True

# For Django template

### In case you dont want to use react appbridge

`add accounts.context_processor.get_shopify_context in the context_processor of the TEMPLATES in the settings`

`include {% include 'includes/redirect_js.html' %} in the call back redirect view template`

### In case you want to use app bridge in djagno template

`include {% include 'incudes/shopify.html' %} in the callback redirect view template `

## If you dont want to use redirect in django template but want to use redirect in react

`add redirectToShopifyAdminPage from the config to the main page/route of the react.`
