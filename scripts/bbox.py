'''
HYU CVLAB
Changhee won
04/20/2017
'''
import os
import os.path as osp
import sys
import math

class Coords:


    def __init__(self, x=0, y=0):
        self.x=x
        self.y=y

    def rotate(self, degree):
        rad = degree * math.pi / 180
        cos = math.cos(rad)
        sin = math.sin(rad)
        x = cos*self.x - sin*self.y
        y = sin*self.x + cos*self.y
        return Coords(x=x, y=y)

    def translate(self, dx, dy):
        return Coords(x=self.x+dx, y=self.y+dy)

class BBox:


    def __init__(self, pose=[0, 0, 0, 0]):
        self.set_bbox(pose)
        self.theta = 0

    def set_bbox(self, pts):
        self.x0 = min(pts[0], pts[2])
        self.y0 = min(pts[1], pts[3])
        self.x1 = max(pts[0], pts[2])
        self.y1 = max(pts[1], pts[3])

    def get_corner_coords(self):
        tl = Coords(x=self.x0, y=self.y0)
        tr = Coords(x=self.x1, y=self.y0)
        bl = Coords(x=self.x0, y=self.y1)
        br = Coords(x=self.x1, y=self.y1)
        cx = (self.x0 + self.x1)/2
        cy = (self.y0 + self.y1)/2
        tl = tl.translate(-cx,-cy).rotate(self.theta).translate(cx,cy)
        tr = tr.translate(-cx,-cy).rotate(self.theta).translate(cx,cy)
        bl = bl.translate(-cx,-cy).rotate(self.theta).translate(cx,cy)
        br = br.translate(-cx,-cy).rotate(self.theta).translate(cx,cy)
        return tl, tr, bl, br

    def translate(self, dx, dy):
        self.x0 += dx
        self.x1 += dx
        self.y0 += dy
        self.y1 += dy

