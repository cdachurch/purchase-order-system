purchase-order-system
=====================

A purchase order system that runs on Google's App Engine, Python flavour. It uses Google apps authentication, and it requires a custom apps domain set in the app settings.

# Local development

Prerequisites:

* [pyenv](https://github.com/pyenv/pyenv) with python 2.7.16 installed like so: `pyenv install 2.7.16`
* [yarn](https://yarnpkg.com/)
* Node 10(+)
* [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) with Python, Python Extras, and Go Extensions plugins installed

Steps:

1. Setup the python2 binary: `pyenv shell 2.7.16`
2. `yarn` to install frontend dependencies
3. `yarn start` to start the dev_appserver.py to run the app
4. In another terminal or process, run `yarn watch-js` to build JS
5. Somehow run the Go api so that you can list purchase orders

# Deployment:

Main app:
Run `yarn deploy:demo` which will build the app and deploy to a demo environment. Confirm that all is well before going to prod!
Run `yarn deploy:prod` which will build the app (again) and deploy to prod 😁

Go API:
Run `yarn deploy:api:demo` which will deploy the go app that serves the list API to demo. You will need to have purchase-order-system-go checked out in the same directory as purchase-order-system for this to work.
Run `yarn deploy:api:prod` to deploy to prod.
