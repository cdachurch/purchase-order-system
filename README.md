# purchase-order-system

A purchase order system that runs on Google's App Engine, Python flavour. It uses Google apps authentication, and it requires a custom apps domain set in the app settings.

## Running the app locally

Most parts of the app work locally with pretty low effort. You'll need to get one file
from the cloud console before you get too far into it, it's the .json file for the service
account that can access the demo environment's Datastore (where the local app points).

### Local dev service account

The service account to use for local dev is aptly named and lives [right here](https://console.cloud.google.com/iam-admin/serviceaccounts/details/102111909895029700743/keys?authuser=0&project=cdac-demo-purchaseorder)! You can add a key to get the json file. Drag it into the root of
the project and rename it to `cdac-demo-purchaseorder-service-account.json`. This is so that
it will be ignored by git (check .gitignore for details there).

### Python virtualenv

Once the json file is in place, you're pretty much set to get the app running. First
though you'll need to activate the python virtualenv. This could be as simple as just
running `.venv\Scripts\activate` (or the non-Windows equivalent), but I'm honestly not
sure at this point how it works on a new computer (todo: try this out!).

### Running the app

`npm start` - this command will set the required environment variables and starts the
flask server with an adhoc ssl cert for using https locally! That's handy for testing
the login flow and such, so we want that for sure.
