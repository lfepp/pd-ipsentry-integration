# PagerDuty - IPSentry Integration

The PagerDuty - IPSentry Integration is an applet that captures an alert output from IPSentry and delivers the alert to PagerDuty.

## Dependencies

* Python (tested on Python 2.7)
* [Requests](http://docs.python-requests.org/en/latest/) >= 1.1.0

## Installation

1. Log onto your IPSentry server

1. Install [Python 2.7](https://www.python.org/downloads/) if it is not already installed

1. Install [Requests](http://docs.python-requests.org/en/latest/user/install/) if it is not already installed

1. Clone the repository into the directory you want this integration to reside:

    ```
    git clone git@github.com:lfepp/pd-ipsentry-integration.git
    ```

## Configuration

1. Create or modify a network monitor that you want to integrate with PagerDuty

1. Under **Settings** -> **Attributes** insert your PagerDuty `integration_key` as **Attribute 9**

1. Under **Alerts** -> **Launch Application** enable the alert status

1. Under **Command Line** enter the following command with **C:\path\to\repo** updated to be the path to the cloned repository:

    ```
    "C:\Windows\System32\cmd.exe" /C"C:\path\to\repo\init.bat -c IPSentry -k ^"%%ca.9%%^" -s ^"%%mach.state%%^" -n ^"%%mach.name%%^" -a ^"%%mach.net.address%%^" --details ^"%%mach.resultinfo%%^" --notes ^"%%mach.notes%%^""
    ```

1. Check the **Trigger on recovery count** checkbox and enter **1** into the field

1. Update your **Alert Schedule** to trigger PagerDuty incidents according to your preferences

## Usage

Once configured, the applet will automatically trigger incidents within PagerDuty when an alert is triggered on one of your IPSentry monitors. Once IPSentry has determined that the monitor has recovered, it will automatically resolve the incident within PagerDuty.

## Credits

1. Nick McLarty <nick@tamu.edu>
1. Luke Epp <lucasfepp@gmail.com>
