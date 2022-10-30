# The Masterpiece Creator
![image](https://user-images.githubusercontent.com/63745301/198887553-9e25daec-aa2f-4e9d-aace-07def8098035.png)

Masterpiece creator uses the [discoart](https://github.com/jina-ai/discoartf) library to create Disco Diffusion artworks.

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

1. Type your prompt into the first input.
2.  Choose the model that suits your prompt best. For example, `portrait_generator_v1.5` and `portrait_generator_v001_ema_0.9999_1MM` are the best options if you want to get a portrait
3. Enter the number of steps (the default is 250; but some models perform best when you run them for way more steps).
4. Hit the Submit button and let it run. The average generation time is about 13 minutes.
