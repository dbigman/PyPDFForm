# PDF coordinates

The coordinate system on a single page of a PDF starts at the bottom left of the page as the origin. The units of 
the coordinates are called "points" and there are 72 points/inch.  PyPDFForm utilizes this coordinate system in 
some of its APIs so that widgets, texts, or images can be created on a PDF.

## Generate a coordinate grid view

To allow a better user experience with the coordinate system, PyPDFForm implements a grid view so that there is a 
better idea on where stuffs should be placed on a PDF.

Consider [this PDF](https://github.com/chinapandaman/PyPDFForm/raw/master/pdf_samples/sample_template.pdf), the 
coordinate grid view can be generated like this:

```python
from PyPDFForm import PdfWrapper

grid_view_pdf = PdfWrapper(
    "sample_template.pdf"
).generate_coordinate_grid(color=(1, 0, 0))

with open("output.pdf", "wb+") as output:
    output.write(grid_view_pdf.read())
```

The `generate_coordinate_grid` method takes one optional parameter `color` which allows you to pick a color for 
the grid view. The default color is red.
