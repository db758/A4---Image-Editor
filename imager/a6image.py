"""
The main class for our imager application.

This modules contains a single class.  Instances of this class support an image
that can be modified.  This is the main class needed to display images in the viewer.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:    October 20, 2017 (Python 3 Version)

Names: Debasmita Bhattacharya (db758) and Myka Umali (meu22)
Date Completed: 15 November 2017
"""
import pixels   # So we can manipulate pixel data
import copy

class Image(object):
    """
    A class that allows flexible access to an image Pixel list.
    
    One of the things that we will see in this assignment is that sometimes you want to
    treat an image as a flat 1D list and other times you want to treat is as a 2D list.
    This class has methods that allow you to go back and forth between the two.
    
    If you want to treat the image like a 2D list, you use the methods `getPixel` and 
    `setPixel`.  As with the Pixels class, pxels are represented as 3-element tuples,
    with each element in the range 0..255.  For example, red is (255,0,0).  These methods
    are used by all of the Instagram-style filter functions.
    
    If you want to treat the image like a 1D list you use the methods `getFlatPixel` and
    `setFlatPixel`.  These methods are used by the steganography methods.
    
    IMMUTABLE ATTRIBUTES (Fixed after initialization)
        _pixels: The underlying list of pixels      [Pixel object]
        _length: The number of pixels in the list   [int >= 0]
    
    MUTABLE ATTRIBUTES (Can be changed at any time)
        _width:  The image width, which is the number of columns [int > 0]
        _height: The image height, which is the number of rows   [int > 0]
    There is an additional invariant that width*height == length at all times.  So
    if you change width, you must change height.
    """

    # IMMUTABLE ATTRIBUTES
    def getPixels(self):
        """
        Returns: the pixel list for this image
        
        This pixel list is used by the GUI to display the image.
        """
        return self._pixels


    def getLength(self):
        """
        Returns: the number of pixels in this image
        """
        return self._length
    
    
    # MUTABLE ATTRIBUTES
    def getWidth(self):
        """
        Returns: The image width
        """
        return self._width 
    
    
    def setWidth(self,value):
        """
        Sets the image width to value, assuming it is valid.
        
        If the width changes, then height must change to so that width*height == length
        This can only happen if the value is valid.
        
        The value is valid if it evenly divides the number of pixels in the image.
        So if the pixel list has 10 pixels, a valid width is 1, 2, 5, or 10.
        
        Parameter value: the new width value
        Precondition: width is an int > 0 and evenly divides the length of pixels
        """
        assert type(value) == int and value > 0 and self.getLength()%value == 0
        
        self._width = value
        self._height = int(self._length//value)
    
    
    def getHeight(self):
        """
        Returns: The image height
        """
        return self._height
    
    
    def setHeight(self,value):
        """
        Sets the image height to value, assuming it is valid.
        
        If the height changes, then width must change to so that width*height == length
        This can only happen if the value is valid.
        
        The value is valid if it evenly divides the number of pixels in the image.
        So if the pixel list has 10 pixels, a valid height is 1, 2, 5, or 10.
        
        Parameter value: the new height value
        Precondition: value is a valid height
        """
        assert type(value) == int and value > 0  and self.getLength()%value == 0
        
        self._height = value
        self._width = int(self._length//value)
    
    
    # INITIALIZER AND OPERATORS
    def __init__(self, data, width):
        """
        Initializer: Creates an Image from the given pixel list.
        
        The pixel list contains the image data.  You do not need to worry about loading
        an image file.  That happens elsewhere in the application (in code that you did
        not write).  However, in order to be a valid initialization, the width must 
        evenly divide the number of pixels in the image. So if the pixel list has 10 
        pixels, a valid width is 1, 2, 5, or 10.
        
        The height is not given explicitly, so you must compute it from the width and
        pixel list length.
        
        Parameter data: The image data as a pixel list
        Precondition: data is a Pixels object
        
        Parameter width: The image width
        Precondition: width is an int > 0 and evenly divides the length of pixels
        """
        assert isinstance(data, pixels.Pixels) 
        assert type(width) == int and width > 0 and len(data)%width == 0
        
 
        self._width = width
        self._pixels = data
        self._length = len(data)
        self._height = int(len(data)//width)
    
    
    def __str__(self):
        """
        Returns: The string representation of this image.
        
        The string should be displayed as a 2D list of pixels in row-major order.  For 
        example, suppose the pixels attribute is 
            
            [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (128, 0, 0), (0, 128, 0)]
        
        If the width (which is the number of columns) is two, the string should be
        
            [[(255, 0, 0), (0, 255, 0)],  [(0, 0, 255), (0, 0, 0)],  [(128, 0, 0), (0, 128, 0)]]
        
        There should be spaces after the commas but nowhere else.  Pixels handle this 
        part for you automatically, so you only need to worry about commas between pixels.
        """
        #where to put commas and square brackets
        #nested for loop
        
        accumulator = '['
        for x in range(self._height):
            accumulator2 = '['
            for y in range(self._width):
                y_as_a_string = str(self.getPixel(x,y))
                accumulator2 = accumulator2 + y_as_a_string + ', '
            accumulator2 = accumulator2[:-2] +']'
            accumulator = accumulator + accumulator2 + ',  '
        accumulator = accumulator[:-3] + ']'
        return accumulator
                
    
    # ACCESS METHODS
    def getPixel(self, row, col):
        """
        Returns: The pixel value at (row, col)
        
        Remember that this way of accessing a pixel is essentially (y,x) since height is 
        the number of rows and width is the number of columns.
        
        The value set is a 3-element tuple (r,g,b).
        
        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height
        
        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width
        
        NOTE: DO enforce the preconditions in this function.
        """
        assert isinstance(row, int)
        assert row >= 0
        assert row < self._height
        assert isinstance(col, int)
        assert col >= 0
        assert col < self._width
        
        #find n
        n = row*self._width + col
        return self._pixels[n]
       
        
    def setPixel(self, row, col, pixel):
        """
        Sets the pixel value at (row, col) to pixel
        
        Remember that this way of setting a pixel is essentially (y,x) since height is 
        the number of rows and width is the number of columns.
        
        The value set is a 3-element tuple (r,g,b).
        
        Parameter row: The pixel row
        Precondition: row is an int >= 0 and < height
        
        Parameter col: The pixel column
        Precondition: col is an int >= 0 and < width
        
        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        
        NOTE: DO NOT enforce the precondition on pixel (let the pixel list handle this for
        you).  DO enforce it on row and col.
        """
        assert isinstance(row, int)
        assert 0 <= row
        assert row < self._height
        assert isinstance(col, int)
        assert 0 <= col
        assert col < self._width
        
        n = row*(self._width) + col
        self._pixels[n] = pixel
        
    
    def getFlatPixel(self, n):
        """
        Returns: Pixel number n of the image (from the underlying pixel list)
        
        This method is used when you want to treat an image as a flat, one-dimensional 
        list rather than a 2-dimensional image.  It is useful for the steganography part 
        of the assignment.
        
        The value returned is a 3-element tuple (r,g,b).
        
        Parameter n: The pixel number to access
        Precondition: n is an int >= 0 and < length (of the pixel list)
        
        NOTE: DO NOT enforce any preconditions.  List the pixel list handle this for you.
        """
        return self._pixels[n]


    def setFlatPixel(self, n, pixel):
        """
        Sets pixel number n of the image (from the underlying pixel list) to pixel
        
        This method is used when you want to treat an image as a flat, one-dimensional 
        list rather than a 2-dimensional image.  It is useful for the steganography part 
        of the assignment.
        
        The value set is a 3-element tuple (r,g,b).
        
        Parameter n: The pixel number to access
        Precondition: n is an int >= 0 and < length (of the pixel list)
        
        Parameter pixel: The pixel value
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        
        NOTE: DO NOT enforce any preconditions.  List the pixel list handle this for you.
        """
        self._pixels[n] = pixel 
    
    
    # ADDITIONAL METHODS
    def swapPixels(self, row1, col1, row2, col2):
        """
        Swaps the pixel at (row1, col1) with the pixel at (row2, col2)
        
        Parameter row1: The pixel row to swap from
        Precondition: row1 is an int >= 0 and < height
        
        Parameter col1: The pixel column to swap from
        Precondition: col1 is an int >= 0 and < width
        
        Parameter row2: The pixel row to swap to
        Precondition: row1 is an int >= 0 and < height
        
        Parameter col2: The pixel column to swap to
        Precondition: col2 is an int >= 0 and < width
        
        NOTE: DO NOT enforce any preconditions here.  They should be enforced already
        in getPixel and setPixel.
        """
       
        newpixel1 = self.getPixel(row2,col2)
        newpixel2 = self.getPixel(row1,col1)
        self.setPixel(row1, col1, newpixel1)
        self.setPixel(row2, col2, newpixel2)
    
    
    def copy(self):
        """
        Returns: A copy of this image object.
        
        This method returns a new Image object. The underlying pixel data must be copied 
        (e.g. the copy cannot refer to the same pixel list object that this file does).
        """
        #new image, new pixel list and a new width
        
        newwidth = self._width
        newdata = self._pixels[:]
        return Image(newdata, newwidth)
        
        #copy_ = copy.deepcopy(self)
        #return copy_

