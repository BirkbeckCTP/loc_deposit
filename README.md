# Library of Congress Deposit Plugin

This deposit plugin is for sending deliveries of eserials to the Library of Congress in response to a Notice for Mandatory Deposit from the U.S. Copyright Office.

## What does it deposit?

For the specified journal and issues the plugin can deposit a zip archive containing the articles of the given issues with:

- PDF
- XML (JATS 1.2, this will send the Galley if there is one or will generate a stub otherwise)
- Any images references in the XML file

## Setup

In order to use this plugin you will need to obtain FTP credentials and a ECDSA key for the server being deposited on.

```
LOC_FTP_SERVER = 'a.server.com'
LOC_FTP_USERNAME = 'ausername'
LOC_FTP_PASSWORD = 'apassword',
LOC_FTP_SERVER_KEY = 'averylongkeywillgohere'
```

Add the above variables to your settings.py file.

## Usage

The deposit process can be invoked on two ways:

1. Via the GUI: Users with Editor/Staff status can select a journal and the issues within that journal to deposit.
2. Via the CLI:

```
python3 manage.py send_to_loc journal_code issue_ids --initial (optional)
```

Here is an example:

```
python3 manage.py send_to_loc olh 123 456 789
```

This will deposit issues 123, 456 and 789

You can also use `--initial` to mark this tranfer as an initial deposit.
