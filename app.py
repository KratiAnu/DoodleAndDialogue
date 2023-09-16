import gradio as gr
from PIL import Image
import os
import openai
from detect_contours import create_final_image
import numpy as np


def get_dialouge(input_situation):
	openai.api_type = "azure"
	openai.api_base = ""
	openai.api_version = ""
	openai.api_key = ""

	response = openai.Completion.create(
	engine="gpt-35-turbo",
	prompt=f"You are comedian bot named mr bean.\n\n###\nUser: Write me four funny dialogs between couple discussing about monthly budget.\nmr bean:  \n(START) ## \nHusband: Honey, I think we need to start budgeting our money better.\nWife: Budgeting? You mean like when you buy a new gadget every month?\nHusband: Well, those are essential gadgets!\nWife: Essential for what? Turning our house into a tech museum?\n(END) ##\n\n###\nUser: Write me four funny dialogs between two friends talking about party.\nmr bean:  \n(START) ##\nJohn: Bro I’ve invited 17 people to watch a movie, would you come?\nBro: ok John, but why so many people?\nJohn: Because the DVD said “Only 18+ viewers.”\nBro: Wait, what?\n(END) ##\n\n### \nUser: Write me four funny dialogs between {input_situation}\nmr bean: \n(START) ##\n",
	temperature=0.7,
	max_tokens=100,
	top_p=0.8,
	frequency_penalty=0,
	presence_penalty=0,
	stop=["(END) ##"])

	output = response.choices[0]['text'].split('\n')

	final_output = []

	for a in output:
		if(a is None or len(a.split(': '))<2):
			continue
		final_output.append(a.split(': ')[1])

	final_output = final_output[:4]
	# pad the dialouge to have 4 lines
	while(len(final_output)<4):
		final_output.append("")
	return final_output

def get_image(input_situation):
	cookie = ""
	os.system(f'python -m BingImageCreator  -U {cookie} --prompt "A 4 panel stick figure comic of two people having a conversation with one thought bubble per panel about {input_situation}" --output-dir bing_image/')
     # read the image saved in bing_image/ folder
	image = np.array(Image.open("bing_image/0.jpeg"))
	return image


def e2e(situation):
	dialouge = get_dialouge(situation)
	image = get_image(situation)
	final_image = create_final_image(image, dialouge)
	return final_image


with gr.Blocks() as demo:
    name = gr.Textbox(label="Situation")
    output = gr.Image(type='pil')
    greet_btn = gr.Button("Greet")
    greet_btn.click(fn=e2e, inputs=name, outputs=output, api_name="e2e")


if __name__ == "__main__":
    demo.launch()