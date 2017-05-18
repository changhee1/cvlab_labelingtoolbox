# cvlab_labelingtoolbox
HYU CVLAB Labeling toolbox

Usage
- command: python run_toolbox.py [dataset]
- e.g.
  - python run_toolbox.py Basketball
  
Dataset Download
- command: python download_dataset.py

Dependencies
- Python 2.7
- Tkinter
- PIL (Python Imaging Library)

Short cut
- <kbd>Drag and drop</kbd> : Draw bbox.
- <kbd>Mouse Right Button</kbd> : Remove bbox.
- <kbd>→, ←, ↑, ↓</kbd> : Move bbox.
- <kbd>Ctrl+z</kbd> : Move bbox to origin pose.
- <kbd>Shift</kbd>+<kbd>→, ←, ↑, ↓</kbd> : Expand bbox.
- <kbd>Ctrl</kbd>+<kbd>→, ←, ↑, ↓</kbd> : Reduce bbox.
- <kbd>Alt</kbd>+<kbd>→, ←</kbd> OR <kbd>Mouse Wheel</kbd> : Rotate bbox
- <kbd>g</kbd> : toggle old groundtruth bbox.
- <kbd>s</kbd> : save and proceed to next image.

