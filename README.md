# Nanoloop Mobile Sample Tools

Very basic audio processing tools.
Targeted for use with [Nanoloop](https://nanoloop.com/) mobile on [iOS](https://nanoloop.com/iphone)/[Android](https://nanoloop.com/android).

Uses `pedalboard` library for audio processing and `streamlit` for the web UI.

Consider supporting me at by grabbing my music on https://gesceap.bandcamp.com/

## Docker

The web app can be deployed on docker.

### Local Build

To build the docker image locally navigate to `nanoloop-mobile-sample-tools` and run:

```sh
docker build -t nanoloop-mobile-sample-tools-local-build .
```

Then run the tagged build `nanoloop-mobile-sample-tools`

```sh
docker run -p 8501:8501 nanoloop-mobile-sample-tools-local-build
```

Then navigate locally in a web browser to:
* http://localhost:8501


### Docker Hub

Docker image available on docker hub.
* https://hub.docker.com/r/gesceap/nanoloop-mobile-sample-tools


To pull then run the app locally on your computer run:

```sh
docker pull gesceap/nanoloop-mobile-sample-tools:latest
docker run -p 8501:8501 nanoloop-mobile-sample-tools:latest
```

Then navigate locally in a web browser to:
* http://localhost:8501


## Streamlit Community Cloud

To use the app on the web, use streamlit community cloud at:
* https://nanoloop-mobile-sample-tools.streamlit.app/


# Development

If you would like to make any additions, submit a pull request to add features.

The web app using `streamlit` is in `app.py` whereas the audio processing is done in the package `nanoloop_mobile_sample_tools`.


## Package

If you would like to install the package and use it

```sh
pip install .
```

Then `import` it in python 

```python
import nanoloop_mobile_sample_tools
```

