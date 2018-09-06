# Marker_Finder_Number
## This is a Python script to find and number the hollow black rings. It will return the location of the center of the rings by an order.
Input Photo
![](https://github.com/Freeshman/Marker_Finder_Number/blob/master/7.png)
Output Photo
![](https://github.com/Freeshman/Marker_Finder_Number/blob/master/result.png)
## Usage
Reference the example.py
## How It works
1.The script converts the image to gry image to find the contour according to the thresh_value
2.Then It removes the contour according to min_area_coef and min_perimeter_coef.
**note**: The min_area_coef and min_perimeter_coef is the ratio of the mean value of area and perimeter respectively. Ex: min_area_coef=1 means the minimum area accepttable is the mean area of the contours.
3.The script will find the up-left ring as the origin of the number.
4.Search the ring along the row direction and then along the col direction, at the same time, the script stores the right order.
5.Return the ordered center of the ring.
