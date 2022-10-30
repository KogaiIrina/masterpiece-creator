# The Masterpiece Creator
![image](https://user-images.githubusercontent.com/63745301/198887553-9e25daec-aa2f-4e9d-aace-07def8098035.png)

Masterpiece creator uses the [discoart](https://github.com/jina-ai/discoartf) library for creating Disco Diffusion artworks.

## Run on the cloud
```bash
lightning run app app.py --cloud
```
## Run locally
```bash
lightning run app app.py
```

## How does it work?

![image](https://user-images.githubusercontent.com/63745301/198887723-af857937-0a6e-4b5f-8a4d-1bd5f09d527a.png)

1. In the first input print your prompt
2. Choose the model what you want to use. For example, `portrait_generator_v1.5` and `portrait_generator_v001_ema_0.9999_1MM` are the best options if you want to get a portrait
3. Output the number of steps (default is 250, but some models require way more steps).
4. Hit the Submit button and wait. The approximate time for waiting is 13 minutes.
