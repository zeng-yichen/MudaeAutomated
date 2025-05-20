# MudaeAutomated
**WORKING IN 2025**

Autos your Mudae rolls, character claims, kakera claims, and other tasks for your Discord account so that you don't have to.
Please remember that self-botting violates Discord's Terms of Service, so automate at your own discretion.

**FEATURES INCLUDE**:
+ rolling to completion every hour
+ claiming any characters with kakera above a prespecified minimum value
+ claiming highest kakera character rolled in the last 45 seconds after rolling to completion **in the last hour before claims reset** (this can be disabled in the config.py file)
+ claiming any kakera spawned from rolls or $mk
+ collecting $dailykakera
+ collecting $daily roll refreshes
+ user monitoring of the internal states of the script through sending simple messages (like "@{replace with your username} list delays") in prespecified Discord channels
+ handling disconnects and reconnects efficiently and reliably

**NOTES ON SCRIPT BEHAVIOR AND ASSUMPTIONS**:
+ assumes $settimer set to 45 seconds
+ assumes $togglesnipe and $togglekakera set to 0

The script will NOT crash or error if these values are different than what they are assumed to be; the script will simply fail to claim/snipe characters protected by these settings.

+ does not assume that automated user account has 5 characters in $likelist (the script **will not** modify the automated user account's $likelist or $wishlist in any way)
+ **NOTE**: Currently, the script only supports automation in ONE (1) channel, but support will expand to multiple channels very very soon

**FEATURES IN DEVELOPMENT INCLUDE**:
+ SLASH COMMANDS
+ automation across multiple channels (need to optimize for lower-end machines)
+ further testing for corner cases
+ more ways to monitor script's internal states

**KNOWN ERRORS**:
+ tasks duplicate in rare cases upon reconnecting

Please contact me through GitHub or at yzeng@berkeley.edu with comments, questions, or suggestions for improvements.

## Setup
Please clone this GitHub repository to your local machine. Instructions for cloning repositories can be found [**HERE**](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

Please install **python 3.11+** if not already installed. Python installation instructions can be found [**HERE**](https://www.python.org/downloads/).\
Once an appropriate python version is installed, run the following command on your local machine **in the MudaeAutomated directory that you cloned**.
```
pip install -r requirements.txt
```
This command installs all the necessary Python libraries for MudaeAutomated.

Next, open the **config.py** file in the MudaeAutomated directory to edit. Fill in values for all of the variables there according to the instructions provided. **Please read the instructions carefully**.

Finally, **in the MudaeAutomated directory**, run the following command.
```
python main.py
```
This command starts the automation script. **Please monitor stdout (the terminal) for the latest updates regarding the script's activities**.
