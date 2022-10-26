import gradio as gr
import lightning as L
from functools import partial
from lightning.app.storage import Drive
from lightning.app.components.serve import ServeGradio

class MasterpieceCreator(ServeGradio):
    inputs = [
      gr.components.Textbox(label="print your prompt here", elem_id="label"),
      gr.components.Dropdown(label="choose you model",
        choices=[
          'PulpSciFiDiffusion',
          'pixel_art_diffusion_hard_256',
          'pixel_art_diffusion_soft_256',
          'pixelartdiffusion4k',
          'watercolordiffusion',
          'watercolordiffusion_2',
          'portrait_generator_v1.5',
          'portrait_generator_v001_ema_0.9999_1MM',
          'FeiArt_Handpainted_CG_Diffusion',
          'Ukiyo-e_Diffusion_All_V1.by_thegenerativegeneration'
        ]),
      gr.components.Number(value=250, label="number of steps"),
    ]
    outputs = gr.components.Image(type="auto", label="Your masterpiece is ready")
    enable_queue = True
    css = '''
      #component-6 {
        flex: 1;
        flex-grow: 1 !important;
      }
      #component-12 {
        flex: 2;
        flex-grow: 2 !important;
      }
      .gradio-container {
        background: white;
      }
      .gr-text-input {
        font-size: 15px;
        border-radius: 6px;
        box-shadow: none;
        hover: 
      }
      .gr-button-primary {
        background: linear-gradient(206.91deg, rgb(121, 46, 229) 16.83%, rgb(62, 171, 179) 144.59%);
        color: white;
        fontsize: 15;
      }
      .gr-button-secondary {
        background: rgb(228, 230, 235);
        transition: background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
          box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms, border-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
          color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
        fontsize: 15;
        color: black;
      }
      .gr-button-lg {
        border-radius: 120px;
      }
      .gr-input:focus {
        border-opacity: 0.5;
        --tw-ring-opacity: 0;
        --tw-border-opacity: 0.5;
        box-shadow: none;
        border-color: rgb(121, 46, 229);
      }
      .gr-input:hover {
        border-color: rgb(121, 46, 229);
      }
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drive_1 = Drive("lit://drive_1")

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

        file_name = f"./img2.png"
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
        gr.Interface(fn=fn, inputs=self.inputs, outputs=self.outputs, examples=self.examples, css=self.css).launch(
            server_name=self.host,
            server_port=self.port,
            enable_queue=self.enable_queue,
        )

app = L.LightningApp(MasterpieceCreator(cloud_compute=L.CloudCompute("gpu")))
