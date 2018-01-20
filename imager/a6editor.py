"""
The primary controller module for the Imager application

This module provides all of the image processing operations that are called whenever you 
press a button. Some of these are provided for you and others you are expected to write
on your own.

Based on an original file by Dexter Kozen (dck10) and Walker White (wmw2)

Author: Walker M. White (wmw2)
Date:    October 20, 2017 (Python 3 Version)

Names: Debasmita Bhattacharya (db758) and Myka Umali (meu22)
Date Completed: 15 November 2017
"""
import a6history


class Editor(a6history.ImageHistory):
    """
    A class that contains a collection of image processing methods
    
    This class is a subclass of ImageHistory.  That means it inherits all of the methods
    and attributes of that class.  We do that (1) to put all of the image processing
    methods in one easy-to-read place and (2) because we might want to change how we 
    implement the undo functionality later.
    
    This class is broken up into three parts (1) implemented non-hidden methods, (2)
    non-implemented non-hidden methods and (3) hidden methods.  The non-hidden methods
    each correspond to a button press in the main application.  The hidden methods are
    all helper functions.
    
    Each one of the non-hidden functions should edit the most recent image in the
    edit history (which is inherited from ImageHistory).
    """
    
    # PROVIDED ACTIONS (STUDY THESE)
    def invert(self):
        """
        Inverts the current image, replacing each element with its color complement
        """
        current = self.getCurrent()
        for pos in range(current.getLength()):
            rgb = current.getFlatPixel(pos)
            red   = 255 - rgb[0]
            green = 255 - rgb[1]
            blue  = 255 - rgb[2]
            rgb = (red,green,blue) # New pixel value
            current.setFlatPixel(pos,rgb)
    
    
    def transpose(self):
        """
        Transposes the current image
        
        Transposing is tricky, as it is hard to remember which values have been changed 
        and which have not.  To simplify the process, we copy the current image and use
        that as a reference.  So we change the current image with setPixel, but read
        (with getPixel) from the copy.
        
        The transposed image will be drawn on the screen immediately afterwards.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,row))
    
    
    def reflectHori(self):
        """
        Reflects the current image around the horizontal middle.
        """
        current = self.getCurrent()
        for h in range(current.getWidth()//2):
            for row in range(current.getHeight()):
                k = current.getWidth()-1-h
                current.swapPixels(row,h,row,k)
    
    
    def rotateRight(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(original.getHeight()
                                                           -col-1,row))
    
    
    def rotateLeft(self):
        """
        Rotates the current image left by 90 degrees.
        
        Technically, we can implement this via a transpose followed by a vertical
        reflection. However, this is slow, so we use the faster strategy below.
        """
        current  = self.getCurrent()
        original = current.copy()
        current.setWidth(current.getHeight())
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                current.setPixel(row,col,original.getPixel(col,original.getWidth()
                                                           -row-1))
    
    
    # ASSIGNMENT METHODS (IMPLEMENT THESE)
    def reflectVert(self):
        """ 
        Reflects the current image around the vertical middle.
        """
        current = self.getCurrent()
        for h in range(current.getHeight()//2):
            for col in range(current.getWidth()):
                k = current.getHeight()-1-h
    
                current.swapPixels(h,col,k,col)
    
    
    def monochromify(self, sepia):
        """
        Converts the current image to monochrome, using either greyscale or sepia tone.
        
        If `sepia` is False, then this function uses greyscale.  It removes all color 
        from the image by setting the three color components of each pixel to that pixel's 
        overall brightness, defined as 
            
            0.3 * red + 0.6 * green + 0.1 * blue.
        
        If sepia is True, it makes the same computations as before but sets green to
        0.6 * brightness and blue to 0.4 * brightness.
        
        Parameter sepia: Whether to use sepia tone instead of greyscale.
        Precondition: sepia is a bool
        """
        if sepia == False:
            current = self.getCurrent()
            for pos in range(current.getLength()): 
                rgb = current.getFlatPixel(pos)
                red   = rgb[0]
                green = rgb[1]
                blue  = rgb[2]
                brightness = 0.3 * red + 0.6 * green + 0.1 * blue
                rgb = (int(brightness),int(brightness),int(brightness)) # New pixel value
                current.setFlatPixel(pos,rgb)
        elif sepia == True:
            current = self.getCurrent()
            for pos in range(current.getLength()): 
                rgb = current.getFlatPixel(pos)
                red   = rgb[0]
                green = rgb[1]
                blue  = rgb[2]
                brightness = 0.3 * red + 0.6 * green + 0.1 * blue
                rgb = (int(brightness),int(0.6*brightness),int(0.4*brightness)) # New pixel value
                current.setFlatPixel(pos,rgb)
    
    
    def jail(self):
        """
        Puts jail bars on the current image
        
        The jail should be built as follows:
        * Put 3-pixel-wide horizontal bars across top and bottom,
        * Put 4-pixel vertical bars down left and right, and
        * Put n 4-pixel vertical bars inside, where n is (number of columns - 8) // 50.
        
        The n+2 vertical bars should be as evenly spaced as possible.
        """
        current = self.getCurrent()
        self._drawHBar(int(0.0), (255,0,0))
        self._drawHBar(current.getHeight()-3, (255,0,0))
        self._drawVBar(int(0.0), (255,0,0))
        self._drawVBar(current.getWidth()-4, (255,0,0))

        numofcols = current.getWidth()
        n = (numofcols - 8) // 50
        betweenbars = 50

        y = 4 + betweenbars
        
        for x in range(n):     
            if y < current.getWidth() - 4:
                self._drawVBar(y, (255,0,0))
                y =  y + betweenbars + 4
        
          
    def vignette(self):
        """
        Modifies the current image to simulates vignetting (corner darkening).
        
        Vignetting is a characteristic of antique lenses. This plus sepia tone helps
        give a photo an antique feel.
        
        To vignette, darken each pixel in the image by the factor
        
            1 - (d / hfD)^2
        
        where d is the distance from the pixel to the center of the image and hfD 
        (for half diagonal) is the distance from the center of the image to any of 
        the corners.
        """
        import pixels
        
        current = self.getCurrent()
        middlerow = current.getWidth()//2
        middlecol = current.getHeight()//2
        hfD = (current.getWidth()**2 + current.getHeight()**2)**0.5
        
        for row in range(current.getHeight()):
            for col in range(current.getWidth()):
                currentpixel = current.getPixel(row, col)
                drow = (row - middlerow)**2
                dcol = (col - middlecol)**2
                d = (drow + dcol)**0.5
                vigt = 1 - (d/hfD)**2
                
                darkred   = currentpixel[0] * vigt
                darkgreen = currentpixel[1] * vigt
                darkblue  = currentpixel[2] * vigt 
                
                vignette = (int(darkred),int(darkgreen),int(darkblue))
                current.setPixel(row, col, vignette)
                #current.setFlatPixel(pos,rgb) 
    
    
    def pixellate(self,step):
        """
        Pixellates the current image to give it a blocky feel.
        
        To pixellate an image, start with the top left corner (e.g. the first row and
        column).  Average the colors of the step x step block to the right and down
        from this corner (if there are less than step rows or step columns, go to the
        edge of the image). Then assign that average to ALL of the pixels in that block.
        
        When you are done, skip over step rows and step columns to go to the next 
        corner pixel.  Repeat this process again.  The result will be a pixellated image.
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        assert isinstance(step, int)
        assert step > 0
        
        current = self.getCurrent()
        
        for y in range(0, current.getWidth(), step):
            for x in range(0, current.getHeight(), step):
                    self._average(x, y, step)
                
        
    def encode(self, text):
        """
        Returns: True if it could hide the given text in the current image; False otherwise.
        
        This method attemps to hide the given message text in the current image.  It uses
        the ASCII representation of the text's characters.  If successful, it returns
        True.
        
        If the text has more than 999999 characters or the picture does not have enough
        pixels to store the text, this method returns False without storing the message.
        
        Parameter text: a message to hide
        Precondition: text is a string
        """
        assert isinstance(text, str) and len(text) !=0
        current = self.getCurrent()
        maxlen = 999999 
        if len(text) > maxlen or len(text) > (current.getLength()):
            return False
        else:
            #our starting marker is chr(777) for two pixels in a row before the start of the message
            self._encode_starter()
            pos = 2
            for x in text:
                num = ord(x)
                self._encode_pixel(num, pos)
                pos = pos +1
            pos_end = len(text) + 2
            for x in range(pos_end, pos_end+2):
                rgb = current.getFlatPixel(x)
                red   = rgb[0]
                green = rgb[1]
                blue  = rgb[2]
                encoded_red3 = ((red // 10) * 10) + 7
                encoded_green3 = ((green // 10) * 10) + 7
                encoded_blue3 = ((blue // 10) * 10) + 7
                if encoded_red3 > 255:
                    encoded_red3 = encoded_red3 - 10
                if encoded_green3 > 255:
                    encoded_green3 = encoded_green3 - 10
                if encoded_blue3 > 255:
                    encoded_blue3 = encoded_blue3 - 10
                current.setFlatPixel(x, (encoded_red3, encoded_green3,
                                         encoded_blue3))
                
            return True 


    def decode(self):
        """
        Returns: The secret message stored in the current image. 
        
        If no message is detected, it returns None
        """
        current = self.getCurrent()
        
        first = current.getFlatPixel(0)
        second = current.getFlatPixel(1)
        
        red1 = first[0]
        green1 = first[1]
        blue1 = first[2]
        
        red2 = second[0]
        green2 = second[1]
        blue2 = second[2]
        
        message = ""
        x = 2
        
        if red1%10 == green1%10 == blue1%10 == red2%10 == green2%10 == blue2%10 == 7:
            while x < current.getLength():
                #current_pix = current.getFlatPixel(x)
                message = message + chr(self._decode_pixel(x))
                x = x + 1
                if self._find_end(x) == True:
                    return message
        else:
            return None 
    
    
    # HELPER FUNCTIONS
    def _drawHBar(self, row, pixel):
        """
        Draws a horizontal bar on the current image at the given row.
        
        This method draws a horizontal 3-pixel-wide bar at the given row of the current
        image. This means that the bar includes the pixels row, row+1, and row+2.
        The bar uses the color given by the pixel value.
        
        Parameter row: The start of the row to draw the bar
        Precondition: row is an int, with 0 <= row  &&  row+2 < image height
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        for col in range(current.getWidth()):
            current.setPixel(row, col, pixel)
            current.setPixel(row+1, col, pixel)
            current.setPixel(row+2, col, pixel)
            
    
    def _drawVBar(self, col, pixel):
        """
        Draws a vertical bar on the current image at the given col.
        
        This method draws a vertical 4-pixel-wide bar at the given col of the current
        image. This means that the bar includes the pixels col, col+1, col+2 and col+3.
        The bar uses the color given by the pixel value.
        
        Parameter col: The start of the col to draw the bar
        Precondition: col is an int, with 0 <= col  &&  col+2 < image width
        
        Parameter pixel: The pixel color to use
        Precondition: pixel is a 3-element tuple (r,g,b) where each value is 0..255
        """
        current = self.getCurrent()
        for row in range(current.getHeight()):
            current.setPixel(row, col, pixel)
            current.setPixel(row, col+1, pixel)
            current.setPixel(row, col+2, pixel)
            current.setPixel(row, col+3, pixel)
    
    
    def _average(self, row, col, step):
        """
        Returns average RGB values for pixels in block with given dimensions
        step x step. Helper to pixellate.
        
        Parameter row: the starting pixel row
        Precondition: row is an int >= 0 and < height
        
        Parameter col: the starting pixel column
        Precondition: col is an int >= 0 and < width
        
        Parameter step: The number of pixels in a pixellated block
        Precondition: step is an int > 0
        """
        current = self.getCurrent()
        
        totalred = []
        totalgreen = []
        totalblue= []
        
        for y2 in range(col, col + step): 
            if y2 < current.getWidth():
                for x2 in range(row, row + step): 
                    if x2 < current.getHeight():
                        now = current.getPixel(x2, y2)
                        totalred.append(now[0])
                        totalgreen.append(now[1])
                        totalblue.append(now[2])
        
        averagered = int(sum(totalred) / len(totalred))
        averagegreen = int(sum(totalgreen) / len(totalgreen))
        averageblue = int(sum(totalblue) / len(totalblue))
        
        for y3 in range(col, col + step): 
            if y3 < current.getWidth():
                for x3 in range(row, row + step): 
                    if x3 < current.getHeight():
                        current.setPixel(x3, y3, (averagered, averagegreen,
                                                  averageblue))
                        
            
    def _decode_pixel(self, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        
        This function assumes that the value was a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue).
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        rgb = self.getCurrent().getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        return  (red % 10) * 100  +  (green % 10) * 10  +  blue % 10
    
    
    def _encode_pixel(self, n, pos):
        """
        Returns: the number n that is hidden in pixel pos of the current image.
        Hides a number n in pixel pos of the current image.
        
        This function assumes that the value is a 3-digit number encoded as the
        last digit in each color channel (e.g. red, green and blue). It handles
        the pixel overflow probelm by subtracting 10 from the RGB value as this
        does not significantly change the colour but keeps the units position
        digit the same.
        
        Parameter n: a value to hide
        Precondition: n is an int and n is a two or three digit number that is
        greater than 0
        
        Parameter pos: a pixel position
        Precondition: pos is an int with  0 <= p < image length (as a 1d list)
        """
        current = self.getCurrent()
        
        rgb = current.getFlatPixel(pos)
        red   = rgb[0]
        green = rgb[1]
        blue  = rgb[2]
        
        encoded_red = ((red // 10) * 10) + n//100
        encoded_green = ((green // 10) * 10) + ((n%100)//10)
        encoded_blue = ((blue // 10) * 10) + n%10

        if encoded_red > 255:
            encoded_red = encoded_red - 10
        if encoded_green > 255:
            encoded_green = encoded_green - 10
        if encoded_blue > 255:
            encoded_blue = encoded_blue - 10
            
        current.setFlatPixel(pos, (encoded_red, encoded_green, encoded_blue))


    def _encode_starter(self):
        """ Finds the starting marker if there is an encoded message in the
        image self.
        
        If there is an encoded message in the image, this function detects that
        starting markers that indicate as such.
        If there is a starting marker, then there is an encoded message.
        
        Parameter self: the image to check for an encoded message.
        Precondition: self is an Image object.
        """
        
        current = self.getCurrent()
        for x in range(0,2):
                rgb = current.getFlatPixel(x)
                red   = rgb[0]
                green = rgb[1]
                blue  = rgb[2]
            
                encoded_red2 = ((red // 10) * 10) + 7
                encoded_green2 = ((green // 10) * 10) + 7
                encoded_blue2 = ((blue // 10) * 10) + 7
            
                if encoded_red2 > 255:
                    encoded_red2 = encoded_red2 - 10
                if encoded_green2 > 255:
                    encoded_green2 = encoded_green2 - 10
                if encoded_blue2 > 255:
                    encoded_blue2 = encoded_blue2 - 10
            
                current.setFlatPixel(x, (encoded_red2, encoded_green2,
                                         encoded_blue2))
               
                
    def _find_end(self,pos):
        """
        Returns True or False depending on whether the end marker 777 appears
        in two consecutive pixels in the image.
        
        The function returns True if the end marker is detected, False if not.
        
        Parameter pos: the current pixel position
        Precondition: pos is an int and pos >= 0 and pos < image length in terms
        of a flattened list
        """
        assert isinstance(pos, int) and pos >= 0
        assert pos < self.getCurrent().getLength()
        
        current = self.getCurrent()
        
        if pos < current.getLength() - 2:
            first = self._decode_pixel(pos)
            unit1 = first%1000
            second = self._decode_pixel(pos+1)
            unit2 = second%1000 
            if unit1 == unit2 == 777:
                return True
            else: return False
        else:
            return False 
    