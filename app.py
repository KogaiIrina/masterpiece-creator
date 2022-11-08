import gradio as gr
import lightning as L
import urllib.parse
from functools import partial
from lightning.app.storage import Drive
from lightning.app.components.serve import ServeGradio

class MasterpieceCreator(ServeGradio):
    inputs = [
      gr.components.Textbox(label="print your prompt here", elem_id="label"),
      gr.components.Dropdown(label="choose you model",
        choices=[
          "PulpSciFiDiffusion",
          "pixel_art_diffusion_hard_256",
          "pixel_art_diffusion_soft_256",
          "pixelartdiffusion4k",
          "watercolordiffusion",
          "watercolordiffusion_2",
          "portrait_generator_v1.5",
          "portrait_generator_v001_ema_0.9999_1MM",
          "FeiArt_Handpainted_CG_Diffusion",
          "Ukiyo-e_Diffusion_All_V1.by_thegenerativegeneration"
        ]),
      gr.components.Number(value=250, label="number of steps"),
    ]
    outputs = gr.components.Image(type="auto", label="Your masterpiece is ready")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drive_1 = Drive("lit://drive_1")
        with open("style.css", "r") as file:
          self.css = file.read()

    def predict(self, prompt, model, number_of_steps):

        results = self.model.create(
          text_prompts=prompt,
          width_height=[512, 448],
          n_batches=1,
          steps=number_of_steps,
          diffusion_model=model,
          clip_models=["ViT-B-32::openai"],
          clip_guidance_scale=40000,
        )

        encoded_prompt = urllib.parse.quote(prompt.replace(" ", "_"))
        file_name = f"./{encoded_prompt}_{number_of_steps}.png"
        result = results[0]
        result.load_uri_to_image_tensor()
        result.save_image_tensor_to_file(file_name)
        self.drive_1.put(file_name)
        return result.tensor

    def build_model(self):
      import discoart
      return discoart

    def run(self, *args, **kwargs):
        if self._model is None:
            self._model = self.build_model()
        fn = partial(self.predict, *args, **kwargs)
        fn.__name__ = self.predict.__name__
        model = gr.Interface(fn=fn, inputs=self.inputs, outputs=self.outputs, examples=self.examples, css=self.css)
        model.queue(concurrency_count=3)
        model.launch(
            server_name=self.host,
            server_port=self.port,
        )

app = L.LightningApp(MasterpieceCreator(cloud_compute=L.CloudCompute("gpu-fast")))
