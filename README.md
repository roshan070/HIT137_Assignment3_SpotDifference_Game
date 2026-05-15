HIT137 Assignment 3 - Spot the Difference Game
==============================================

Files included
--------------
1. spot_the_difference_hd.py  - Main Python program.
2. sample_test_image.png      - Test image for checking the game quickly.
3. requirements.txt           - Required Python packages.
4. github_link.txt            - Paste your public GitHub repository link here.
5. outputs/                   - Example output preview image.

How to install
--------------
Open terminal in this folder and run:

    pip install -r requirements.txt

How to run
----------
Run:

    python spot_the_difference_hd.py

Then click "Load New Image" and select JPG, PNG or BMP file.
You can use sample_test_image.png for testing.

Main implemented features
-------------------------
- Tkinter GUI with menu, toolbar, two image panels and status bar.
- Original image displayed on the left and modified image on the right.
- Only the modified image responds to player clicks.
- OpenCV reads, clones, resizes and manipulates images.
- Exactly 5 difference regions are generated on every image load.
- Random difference type and random position on every image load.
- Non-overlap is checked before each region is accepted.
- Four alteration types are implemented:
  1. Colour shift
  2. Local blur
  3. Brightness change
  4. Subtle shape overlay
- Correct clicks draw red circles on both images.
- Reveal button draws blue circles for all unfound differences on both images.
- Mistake counter updates after each wrong click.
- The round locks after 3 mistakes.
- The round also locks after all 5 differences are found.
- Loading a new image resets current round counters.
- Total found and completed rounds continue across multiple images.

OOP design used
---------------
- DifferenceRegion: stores each hidden region.
- ImageLoader: loads JPG, PNG and BMP images safely.
- Alteration: abstract parent class.
- ColourShiftAlteration, BlurAlteration, BrightnessAlteration and ShapeOverlayAlteration: child classes overriding apply().
- DifferenceGenerator: randomly selects alteration objects and applies them polymorphically.
- GameRound: stores current game state, score, mistakes and image feedback.
- ImagePanel: reusable Tkinter Canvas image panel.
- SpotDifferenceApp: main GUI application.

Notes for submission
--------------------
- Create a public GitHub repository.
- Upload all files from this folder.
- Add all group members to the repository.
- Replace the placeholder text in github_link.txt with the real public GitHub link.
- Zip the programming files, outputs and github_link.txt before uploading to Learnline.
