## Splunk Python Modular Inputs v1.0

# IMPORTANT NOTE :

Although this framework is fully functional and stable, since it was released Splunk have now created their own Python Modular Inputs librarys.
So I recommend that you use the formally Splunk developed and supported offering that can be found here : http://dev.splunk.com/view/python-sdk/SP-CAAAER3

## Overview

This is a simple template based framework for building <a href="http://docs.splunk.com/Documentation/Splunk/latest/AdvancedDev/ModInputsIntro">Splunk Modular Inputs</a> in Python

It contains an example HelloWorld Modular Input that you can use as a practical reference to follow.

## Prerequisites

* Splunk 5+
* Clone the repository and setup a project in your IDE ie: Eclipse

## Initial setup

In the below instructions , "NAME" refers to the name of your new modular input

* Copy the "template" directory to the "implementations" directory and rename it "NAME"
* Set the "NAME" in build/build.properties
* Rename bin/modinput.py to bin/NAME.py

## Implementing your new modular input

Browse to the implementations/NAME directory
There are several placeholders that you have to fill in

* README/inputs.conf.spec
* default/app.conf
* defaults/data/ui/manager/modinput.xml
* appserver/static/appIcon.png
* appserver/static/screenshot.png
* appserver/static/README.md
* bin/NAME.py

## The Python script

From step 7 above , this is where you implement your mod input's core processing logic.
Again , there are just some placeholders you need to fill in.

* fill in the "SCHEME" xml string
* implement the do_validate() function , if you are using external validation
* implement the do_run() function

## Build a release

This will build a SplunkBase compatible release tarball.

* run the Ant target "build_modular_input" in build/build.xml
* the release will get written to the "releases" directory
* copy to $SPLUNK_HOME/etc/apps , untar , restart Splunk, and test away.

## Contact

This project was initiated by Damien Dallimore
<table>

<tr>
<td><em>Email</em></td>
<td>ddallimore@splunk.com</td>
</tr>

<tr>
<td><em>Twitter</em>
<td>@damiendallimore</td>
</tr>


</table>


