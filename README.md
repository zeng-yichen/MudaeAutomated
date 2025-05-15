# MudaeAutomated
**WORKING IN 2025**

Autos your Mudae rolls, character claims, kakera claims, and other tasks for your Discord account so that you don't have to (＾▽＾)\
Please remember that self-botting violates Discord's Terms of Service, so automate at your own discretion.

**AUTOMATED TASKS INCLUDE**:
+ rolling to completion every hour
+ claiming any characters with kakera above a prespecified minimum value
+ claiming any characters with kakera above an (optionally) *different* prespecified minimum value in the last hour before claims refresh
+ claiming any kakera spawned from rolls or $mk
+ collecting $dailykakera
+ collecting $daily roll refreshes

**OTHER FEATURES INCLUDE**:
+ monitoring the internal states of the script through sending simple messages (like "@{replace with your username} list delays") in prespecified Discord channels
+ handling disconnects and reconnects efficiently and reliably

**FEATURES IN DEVELOPMENT INCLUDE**:
+ SLASH COMMANDS
+ automation across multiple channels (need to optimize for lower-end machines)
+ further testing for corner cases
+ more ways to monitor script's internal states

**NOTE**: Currently, the script only supports automation in ONE (1) channel, but support will expand to multiple channels very very soon.\
In addition, the script assumes:
+ $settimer set to 45 seconds
+ $togglesnipe and $togglekakera set to 0
The script will NOT crash or error if these values are different than what they are assumed to be; the script will simply fail to claim/snipe characters protected by these settings.

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

**Enjoy** (＾▽＾)
