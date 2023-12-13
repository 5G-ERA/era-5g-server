# era-5g-server

A server application for 5G-ERA Network Applications. Contains the basic implementation of the server 
([server.py](era_5g_server/server.py)).

## Related Repositories

- [era-5g-client](https://github.com/5G-ERA/era-5g-client) - client classes for 5G-ERA Network Applications with 
  various transport options.
- [era-5g-interface](https://github.com/5G-ERA/era-5g-interface) - python interface (support classes) for Network 
  Applications.
- [Reference-NetApp](https://github.com/5G-ERA/Reference-NetApp) - reference 5G-ERA Network Application implementation 
  with MMCV detector.

## Installation

The package could be installed via pip:

```bash
pip install era_5g_server
```

## Classes

### NetworkApplicationServer ([server.py](era_5g_server/server.py))

Basic implementation of the 5G-ERA Network Application server.
It creates websocket server (socketio.Server, socketio.WSGIApp) and bind callbacks from the 5G-ERA Network Application.

How to send data? E.g.:

    client.send_image(frame, "image", ChannelType.H264, timestamp, encoding_options=h264_options, sid=sid)
    client.send_image(frame, "image", ChannelType.JPEG, timestamp, metadata, sid)
    client.send_data({"message": "message text"}, "event_name", sid)

How to create `callbacks_info`? E.g.:

    {
        "results": CallbackInfoServer(ChannelType.JSON, results_callback),
        "image": CallbackInfoServer(ChannelType.H264, image_callback, error_callback)
    }

Callbacks have sid and data parameter: e.g. `def image_callback(sid: str, data: Dict[str, Any]):`.
Image data dict including decoded frame (`data["frame"]`) and send timestamp (`data["timestamp"]`).

Methods `command_callback` and `disconnect_callback` can can be defined (redefined) within and inherited class or can 
be set by parameters in NetworkApplicationServer class.

## Contributing, development

- The package is developed and tested with Python 3.8.
- Any contribution should go through a pull request from your fork.
- We use Pants to manage the code ([how to install it](https://www.pantsbuild.org/docs/installation)).
- Before committing, please run locally:
  - `pants fmt ::` - format all code according to our standard.
  - `pants lint ::` - checks formatting and few more things.
  - `pants check ::` - runs type checking (mypy).
  - `pants test ::` - runs Pytest tests.
- The same checks will be run within CI.
- A virtual environment with all necessary dependencies can be generated using `pants export ::`. 
  You may then activate the environment and add `era_5g_server` to your `PYTHONPATH`, which is equivalent 
  to installing a package using `pip install -e`.
- To generate distribution packages (`tar.gz` and `whl`), you may run `pants package ::`.
- For commit messages, please stick to
  [https://www.conventionalcommits.org/en/v1.0.0/](https://www.conventionalcommits.org/en/v1.0.0/).
