
#!/usr/bin/env python3

import os
from datetime import datetime
from speech_processing import start_recording, speak
from openai_processing import complete_openai
import rospy
from std_msgs.msg import String



settings = {
    'speechKey': "d14d3ca71c944fb1a045b3dd1d52595b",
    'region': "westeurope",
    'language': "English",
    'openAIKey': "c2e59398051e4e14b2003dd188e548a5"
}

output_folder = f'./Output/{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
os.makedirs(output_folder)

conversation = []
deployment_name='Robin'

while True:
    speech = start_recording()
    if speech == "Robin.":
        break


while True:
    speech = start_recording()
    conversation.append(speech)
    if speech == "Break.":
        break
    prompt = ""
    for i in range(len(conversation)-4, len(conversation)):
        if (i >= 0):
            if (i % 2 == 0):
                prompt += f"Q: {conversation[i]}\n"
            else:
                prompt += f"A: {conversation[i]}\n"
    prompt += "A: "
    result = complete_openai(prompt=prompt)
    print(result)
    
    speak(result, output_folder=output_folder)
    pub = rospy.Publisher('speech', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    pub.publish(result)
    conversation.append(result)



#commit
