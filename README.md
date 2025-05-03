DISCLAIMER: This tool and its contributers are not responsible for what happens to your discord account in any way. Self-botting is a bannable offense and this tool should not be used for any malicious purposes. (I recommend you only use this on an alt and only use it on your friends.)

NOTICE: Currently this only works on windows machines! (Unless you modify how the python script downloads the chrome drivers!) You can easily fix it with a bit of code if you want.

Pre-requisites:

You must have python. (If your copy of python doesnt work then try python 3.10!)

You must have [text-generation-ui](https://github.com/oobabooga/text-generation-webui) fully set up and running (With the --api fflag) in order to use this project in the way it was intended. OpenAI's API may work as well but it has not been tested, and it would require modification of the project.

Here are the recommended settings for text-generation-ui which is what I used on my machine.

```
--api --mlock --n-gpu-layers 40 --nowebui --torch-compile --ctx-size 8000 --model deepseek-llm-7b-chat.Q6_K.gguf --character Assistant
``` 
##-- WARNING! You will most likely need to modify --n-gpu-layers as that is how many layers will be sent to the gpu and if you have a small gpu or no gpu it will either crash or lag you really bad. For users with no GPU, you will need to use text-generation-ui's CPU mode.

You can get LLM's off of [huggingface](https://huggingface.co/TheBloke/deepseek-llm-7B-chat-GGUF) for text-generation-ui.


Shoutouts and credits:

Major shoutout to [text-generation-ui](https://github.com/oobabooga/text-generation-webui), oobabooga, and all the other contributors to their project! It's
only because of them that this project was possible!

Shoutout to Selenium for providing me with an API to interface with chrome therefore allowing me to interact with discord.

Credits to me for writing the main script.