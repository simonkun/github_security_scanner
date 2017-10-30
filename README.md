# GitHub Security Scanner

This is a tool used to scan an organization's GitHub repositories to check for any security issues.

## Assumptions

* The organization being scanned already has a 'quarantine' team setup that has restricted user access
* You have a user account that is a member of the organization

## Getting Started

Using the GitHub Security Scanner is easy! Once setup use like this:

```
python .\main.py GitHub_Organisation_Name
```

You will then be prompted for your username and password - enter these and the scan will commence!

There is some in built help if you need it!

## Prerequisites

In order to run this you need Python (Version 3.6 recommended) and you will need the Requests library (Version 2.18.4 recommended) Get these from here:

```
Python is available from https://www.python.org/
```
```
The Python Requests library is available from http://docs.python-requests.org/en/master/
```

## Improvements/Extensions/TODO

Still a bunch more can be done!
* Certificate authentication - make sure we are connecting to the legit GitHub
* Feedback to user on authentication failure
* Better response & error checking
* Logging - only logging success at the moment
* Look at webhooks
* Look at new users - maybe local database?
* Be efficent with users already quarantined (currently we remove and re-add)

## Authors

* **Simon Kun** - [GitHub](https://github.com/simonkun)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Contentful for the opportunity!
