import requests
import json
from flask import Flask, render_template
from player import get_player_ids
import os
import pickle

player_ids = get_player_ids()
print(player_ids)
