import gradio as gr
import lightning as L
from lightning.app.components.serve import ServeGradio

class MasterpieceCreator(ServeGradio):
    inputs = gr.inputs.Textbox(label="print your prompt here")
    outputs = gr.outputs.Image(type="auto", label="Your masterpiece is ready")
    enable_queue = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def predict(self, prompt):
        da = self.model.create(
          text_prompts=prompt,
          width_height=[512, 512],
          n_batches=1,
        )
        da[0].load_uri_to_image_tensor()
        return da[0].tensor

    def build_model(self):
      import discoart
      return discoart


app = L.LightningApp(MasterpieceCreator(cloud_compute=L.CloudCompute("gpu-fast")))
