# USE GOOGLE COLLAB

# from huggingface_hub import notebook_login
# notebook_login()


# from diffusers import StableDiffusionPipeline
# import torch
# 
# # Load the model
# model_id = "CompVis/stable-diffusion-v1-4"
# pipe = StableDiffusionPipeline.from_pretrained(model_id)
# pipe = pipe.to("cuda")  # Use GPU for faster processing


# prompt = "beach"
# camera_angle = "wide-shot"
# full_prompt = f"{camera_angle} of {prompt}"
#
# image = pipe(full_prompt).images[0]
#
# # Save and display the image
# image.save("generated_image3.png")
# image.show()
