# Code for Send Crop Weather Alerts Learn module

This is the code used in the Learn module "Send Crop Weather Alerts"

## How to Deploy

1. Create a new Python Azure Functions app
1. In the Function app's storage account create a Table with name `alerts`
1. Create an Azure Maps Account and obtain your primary API key
1. [Create a Twilio account](https://twilio.com/azure) and a SMS capable phone number. Get your Twilio AccountSID and AuthToken and the Twilio Phone Number.
1. Create the following App Settings in the Function App

    ```
        "AZURE_MAPS_SUBSCRIPTION_KEY": "<YOUR AZURE MAPS KEY HERE>",
        "TwilioAccountSID": "<YOUR TWILIO ACCOUNTSID HERE>",
        "TwilioAuthToken": "<YOUR TWILIO ACCOUNT AUTH TOKEN HERE>",
        "TWILIO_PHONE_NUMBER": "<YOUR TWILIO PHONE NUMBER HERE, e.g. +12223334444>"
    ```
1. Deploy this repo to your function app.
1. Get the Function URL for the `SetupAlert` endpoint (with the Function Key included)
1. In the Twilio console, go to the Phone Number management setting and add a webhook for SMS messages with the URL from the previous step.

Now you are ready to use the app by sending a SMS to your Twilio number!

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
