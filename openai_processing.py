from openai import AzureOpenAI
import os
import requests


client = AzureOpenAI(
    api_key= "c2e59398051e4e14b2003dd188e548a5",  
    api_version= "2024-02-01",
    azure_endpoint = "https://cobotmakerspace.openai.azure.com/"
    )


def complete_openai(prompt):

    try:
        response = client.chat.completions.create(model="Robin", messages=[{"role":"user", "content": prompt}])
        return(response.choices[0].message.content)
    except Exception as e:
        print("An exception of type", type(e), "occurred with the message:", e)
        return "Sorry, I couldn't process your request"
    

#commit
