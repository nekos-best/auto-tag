# Auto-Tag for Anime Images
Original code by [Epsp0](https://github.com/Epsp0) in [auto-tag-anime](https://github.com/Epsp0/auto-tag-anime)\
Model provided by [KichangKim](https://github.com/KichangKim) in [DeepDanbooru](https://github.com/KichangKim/DeepDanbooru)

## Requrements
- Python 3.10

## Instructions
1. **Download the model**: Download from [Google Drive](https://drive.google.com/file/d/1qffwjF-BHV6MkPVliLO1jZwMQatri06v) or [DeepDanbooru](https://github.com/KichangKim/DeepDanbooru) and place it in the `./model` folder.
2. **Install dependencies**: Run the following command to install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
```bash
python3 auto-tag.py "/path/to/directory/"`
```

## Important Disclaimer

**Do not modify `tags.txt`**: This file contains all possible tags used by the model and must remain unchanged to ensure the model functions correctly.

**Modify only `metadata.txt`**: If you want to control which tags should be included in the JSON output, edit the `metadata.txt` file. Add or remove tags from this file to customize the tags that will be saved to the JSON.
