import json

def modify_anime_data(file_path):
  with open(file_path, "r") as f:
    anime_data = json.load(f)

  # Add id property with increasing values
  for i, anime in enumerate(anime_data):
    anime["id"] = i

  # Write updated data back to the file
  with open(file_path, "w") as f:
    json.dump(anime_data, f, indent=4)

if __name__ == "__main__":
  file_path = "animes.json"  # Replace with your actual file path
  modify_anime_data(file_path)
  print(f"Added 'id' property to {file_path} and updated the file.")