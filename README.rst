****************************
Intelligent Music Visualizer
****************************

An intelligent music visualiser, generating animations based on audio inputs.

.. contents:: **Table of contents**

Features
~~~~~~~~

* Generates animation based on audio beats
* Support real time input
* Support audio input from a file
* [WIP] Varying animations based on lyrics and sentiment analysis

Requirements
~~~~~~~~~~~~

* Python versions: >=3.6, <=3.8

Installation
~~~~~~~~~~~~

Install directly from this repository, execute the following in repository root directory

``python setup.py install``


Usage
~~~~~

.. code-block:: console

    $ intelligent_visualiser --help
        usage: intelligent_visualiser [-h] [--log_level LOG_LEVEL]
                                      [--duration DURATION] [--fps FPS] [--save]
                                      [--speed SPEED] [--video_file VIDEO_FILE]
                                      [--output_file OUTPUT_FILE]
                                      {live_input,data_input} ...

        CLI for Intelligent Music visualizer

        optional arguments:
          -h, --help            show help messages for the commands (...sub commands)
          --log_level LOG_LEVEL
                                Logging level
          --duration DURATION   Duration in seconds
          --fps FPS             FPS
          --save                Save animation
          --speed SPEED         Animation speed
          --video_file VIDEO_FILE
                                Animation file output path
          --output_file OUTPUT_FILE
                                Video only file output path

        Modes:
          {live_input,data_input}
            live_input          Record audio data and process it
            data_input          Loads data from a file and process it

* NOTE: make sure directory ``~/intelligent_visualiser`` is not reserved. To override default, specify directory in environment var ``INTELLIGENT_VISUALIZER_OUT``

Examples Commands
~~~~~~~~~~~~~~~~~

1. Save animation from live audio input
---------------------------------------

.. code-block:: console

    $ intelligent_visualiser --save --duration=5 live_input


.. image:: ./media/images/save_example.gif
    :height: 400px
    :width: 400 px
    :align: center


Output in ``~/intelligent_visualiser/animation_output.mp4``

2. Plot animation from live audio input
---------------------------------------

.. code-block:: console

    $ intelligent_visualiser --duration=5 live_input --duration=5


3. Save animation from audio data from a file
---------------------------------------------

.. code-block:: console

    $ intelligent_visualiser --save --duration=5 data_input --music_file FILE_PATH



TODOs
~~~~~

* Lyrics engine
* Sentiment analytics
* Documentation
