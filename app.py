import gradio as gr
import lightning_app as L
from lightning_app.components.serve import ServeGradio

class MasterpieceCreator(ServeGradio):
    inputs = gr.inputs.Textbox(label="print your prompt here")
    outputs = gr.outputs.Image(type="auto", label="Your masterpiece is ready")
    enable_queue = True

    def predict(self, prompt):
        results = self.model.create(
          text_prompts=prompt,
          width_height=[512, 512],
          n_batches=1,
        )
        result = results[0]
        result.load_uri_to_image_tensor()
        return result.tensor

    def build_model(self):
      import discoart
      return discoart


app = L.LightningApp(MasterpieceCreator(cloud_compute=L.CloudCompute("gpu")))
