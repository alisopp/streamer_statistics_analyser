#!/bin/bash
python /twitch_reader/base_generator.py
mv /twitch_reader/example_website/data.js /wwwroot
crond -f
