/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-c9au--k3.us', // the auth0 domain prefix
    audience: 'drink_page', // the audience set for the auth0 app
    clientId: '1ETyj5ksRFAp1b1mCgpy4i2MEHZAHWO6', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
