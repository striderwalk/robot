import json

dat = {
  "board": [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0],    
    [2, 1, 1, 0, 1, 3],
    [0, 0, 0, 0, 0, 0],
],

  "size": {
    "width": 6,
    "height": 7
  }
}

with open("./levels/level_one.json", "w") as file:
    json.dump(dat, file)
