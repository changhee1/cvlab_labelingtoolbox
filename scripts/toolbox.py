'''
HYU CVLAB
Changhee won
04/20/2017
'''
import os
import os.path as osp
import sys
import math

import Tkinter as tk
from PIL import Image, ImageTk

from cfg import CFG
from .bbox import BBox, Coords

class BBLabelingToolBox:


    def __init__(self, dbname):
        self.dbname = dbname
        self.img_path = []
        self.n_imgs = 0
        self.img_idx = 0
        
        self.db_path = osp.join(CFG['DATA_DIR'], dbname, 'img')
        self.img_list = sorted([f for f in os.listdir(self.db_path) if any(
            f.endswith(ext) for ext in CFG['IMG_EXTS'])])
        self.img_path = map(lambda x : osp.join(
            self.db_path, x), self.img_list)
        self.n_imgs = len(self.img_path)
        self.gtlist = self._load_old_gt()
        self.draw_gt = True

        self._root = tk.Tk()
        self.scr_w = self._root.winfo_screenwidth()
        self.scr_h = self._root.winfo_screenheight()
        self.canvas = tk.Canvas(self._root, cursor='tcross',
            bd=0, highlightthickness=0)
        self.canvas.grid(row = 0, column = 0)
        self.canvas_bg_id = 0
        self.canvas_bb_id = [0, 0, 0, 0]
        self.canvas_gt_bb_id = [0, 0, 0, 0]
        self.mouse_poses = []
        self.current_bbox = BBox()
        self._bind_events()

    def start(self):
        self._display_img(self.img_path[0])
        self._draw_gt_bbox()
        self._root.mainloop()

    def _load_old_gt(self):
        gtfile = osp.join(CFG['DATA_DIR'], self.dbname, 'groundtruth_rect.txt')
        with open(gtfile) as f:
            gtlines = f.readlines()
            splitchars = ['\t', ',', ' ']
            gtlist = []
            for line in gtlines:
                for c in splitchars:
                    if c in line:
                        gtlist.append(map(int,line.strip().split(c)))
            return gtlist

    def _bind_events(self):
        root = self._root
        root.bind("<Escape>", lambda e: e.widget.quit())
        root.bind("s", self._save_and_next_img)
        root.bind("<Control-z>", self._undo_bbox)
        root.bind("<g>", self._toggle_gt)
        root.bind("<Up>", lambda e: self._move_bbox_key(e, 'up'))
        root.bind("<Down>", lambda e: self._move_bbox_key(e, 'down'))
        root.bind("<Left>", lambda e: self._move_bbox_key(e, 'left'))
        root.bind("<Right>", lambda e: self._move_bbox_key(e, 'right'))
        root.bind("<Shift-Up>", lambda e: self._aspect_bbox(e, 'up', 1))
        root.bind("<Shift-Down>", lambda e: self._aspect_bbox(e, 'down', 1))
        root.bind("<Shift-Left>", lambda e: self._aspect_bbox(e, 'left', 1))
        root.bind("<Shift-Right>", lambda e: self._aspect_bbox(e, 'right', 1))
        root.bind("<Control-Up>", lambda e: self._aspect_bbox(e, 'up'))
        root.bind("<Control-Down>", lambda e: self._aspect_bbox(e, 'down'))
        root.bind("<Control-Left>", lambda e: self._aspect_bbox(e, 'left'))
        root.bind("<Control-Right>", lambda e: self._aspect_bbox(e, 'right'))
        root.bind("<Alt-Left>", lambda e: self._rotate_bbox(
            e, -CFG['ROTATE_STEP']))
        root.bind("<Alt-Right>", lambda e: self._rotate_bbox(
            e, CFG['ROTATE_STEP']))
        self.canvas.bind("<Button-1>", self._onclick_img)
        self.canvas.bind("<Button-3>", self._reset_bbox)
        self.canvas.bind("<Motion>", self._move_mouse)
        self.canvas.bind("<ButtonRelease-1>", self._onclick_img)
        root.bind("<MouseWheel>",  lambda e: self._rotate_bbox(e, 0))
        # root.bind("<Button-4>", lambda e: self._rotate_bbox(e, -1))
        # root.bind("<Button-5>", lambda e: self._rotate_bbox(e, 1))

    def _onclick_img(self, e):
        x = e.x
        y = e.y
        if len(self.mouse_poses) == 4:
            self._reset_bbox(e)

        if [x, y] == self.mouse_poses:
            self._reset_bbox(e)
            return

        self.mouse_poses += [x, y]
        if len(self.mouse_poses) == 4:
            self.current_bbox.set_bbox(self.mouse_poses)
            self._draw_bbox()

    def _move_mouse(self, e):
        if len(self.mouse_poses) == 2:
            self.current_bbox.set_bbox(self.mouse_poses+[e.x,e.y])
            self._draw_bbox()

    def _display_img(self, img):
        im = Image.open(img)
        (w, h) = im.size
        self.current_imtk = ImageTk.PhotoImage(im)
        if self.canvas_bg_id == 0:
            self.canvas_bg_id = self.canvas.create_image(
                0, 0, image=self.current_imtk, anchor='nw')
        else:
            self.canvas.itemconfig(self.canvas_bg_id, image=self.current_imtk)
        self._root.geometry('%dx%d+%d+%d'%(w,h+50,
            (self.scr_w-w)/2,(self.scr_h-h-50)/2))
        self.canvas.config(width=w, height=h)

    def _save_and_next_img(self, e):
        if len(self.mouse_poses) == 4:
            x0 = self.current_bbox.x0
            y0 = self.current_bbox.y0
            x1 = self.current_bbox.x1
            y1 = self.current_bbox.y1
            theta = self.current_bbox.theta
            out_path = osp.join(CFG['OUT_DIR'], self.dbname)
            if not osp.exists(out_path):
                os.mkdir(out_path)
            out_file = osp.join(out_path,
                self.img_list[self.img_idx][:-4] + '.txt')
            f = open(out_file, 'w')
            f.write('%d %d %d %d %d\n' % (x0, y0, x1, y1, theta))
            f.close()
            print 'wrote "%d %d %d %d %d" to "%s".' % (
                x0, y0, x1, y1, theta, out_file)
            if self.img_idx < self.n_imgs - CFG['LABEL_STEP']:
                # self._reset_bbox(e)
                self.img_idx += CFG['LABEL_STEP']
                self._display_img(self.img_path[self.img_idx])
                self._draw_gt_bbox()
            else:
                sys.exit('done\n')

    def _toggle_gt(self, e):
        self.draw_gt = not self.draw_gt
        if not self.draw_gt:
            [self.canvas.delete(self.canvas_gt_bb_id[x]) for x in range(4)]
            self.canvas_gt_bb_id = [0,0,0,0]
        else:
            self._draw_gt_bbox()
        

    def _draw_bbox(self, fill='blue', width=2):
        tl, tr, bl, br = self.current_bbox.get_corner_coords()
        if sum(self.canvas_bb_id) != 0:
            self.canvas.coords(self.canvas_bb_id[0], tl.x, tl.y, tr.x, tr.y)
            self.canvas.coords(self.canvas_bb_id[1], bl.x, bl.y, br.x, br.y)
            self.canvas.coords(self.canvas_bb_id[2], tl.x, tl.y, bl.x, bl.y)
            self.canvas.coords(self.canvas_bb_id[3], tr.x, tr.y, br.x, br.y)
        else:
            self.canvas_bb_id[0] = self.canvas.create_line(
                tl.x,tl.y,tr.x,tr.y, fill=fill, width=width)
            self.canvas_bb_id[1] = self.canvas.create_line(
                bl.x,bl.y,br.x,br.y, fill=fill, width=width)
            self.canvas_bb_id[2] = self.canvas.create_line(
                tl.x,tl.y,bl.x,bl.y, fill=fill, width=width)
            self.canvas_bb_id[3] = self.canvas.create_line(
                tr.x,tr.y,br.x,br.y, fill=fill, width=width)

    def _draw_gt_bbox(self, fill='green', width=2, dash=(3,5)):
        if not self.draw_gt:
            return
        gt = self.gtlist[self.img_idx]
        gtpose = [gt[0], gt[1], gt[0]+gt[2], gt[1]+gt[3]]
        gtbbox = BBox(pose=gtpose)
        tl, tr, bl, br = gtbbox.get_corner_coords()
        if sum(self.canvas_gt_bb_id) != 0:
            self.canvas.coords(self.canvas_gt_bb_id[0], tl.x, tl.y, tr.x, tr.y)
            self.canvas.coords(self.canvas_gt_bb_id[1], bl.x, bl.y, br.x, br.y)
            self.canvas.coords(self.canvas_gt_bb_id[2], tl.x, tl.y, bl.x, bl.y)
            self.canvas.coords(self.canvas_gt_bb_id[3], tr.x, tr.y, br.x, br.y)
        else:
            self.canvas_gt_bb_id[0] = self.canvas.create_line(
                tl.x,tl.y,tr.x,tr.y, fill=fill, width=width, dash=dash)
            self.canvas_gt_bb_id[1] = self.canvas.create_line(
                bl.x,bl.y,br.x,br.y, fill=fill, width=width, dash=dash)
            self.canvas_gt_bb_id[2] = self.canvas.create_line(
                tl.x,tl.y,bl.x,bl.y, fill=fill, width=width, dash=dash)
            self.canvas_gt_bb_id[3] = self.canvas.create_line(
                tr.x,tr.y,br.x,br.y, fill=fill, width=width, dash=dash)

    def _undo_bbox(self, e):
        if len(self.mouse_poses) == 4:
            self.current_bbox.theta = 0
            self.current_bbox.set_bbox(self.mouse_poses)
            self._draw_bbox()

    def _reset_bbox(self, e):
        if sum(self.canvas_bb_id) != 0:
            [self.canvas.delete(self.canvas_bb_id[x]) for x in range(4)]
        self.canvas_bb_id = [0,0,0,0]
        self.mouse_poses = []
        self.current_bbox.set_bbox([0,0,0,0])
        self.current_bbox.theta = 0

    def _move_bbox_key(self, e, direction):
        if len(self.mouse_poses) == 4:
            if direction == 'up':
                dx = 0
                dy = -CFG['MOVE_STEP']
            elif direction == 'down':
                dx = 0
                dy = CFG['MOVE_STEP']
            elif direction == 'left':
                dx = -CFG['MOVE_STEP']
                dy = 0
            elif direction == 'right':
                dx = CFG['MOVE_STEP']
                dy = 0
            self.current_bbox.translate(dx,dy)
            self._draw_bbox()

    def _aspect_bbox(self, e, direction, grow=0):
        if len(self.mouse_poses) == 4:
            if direction == 'up':
                if grow == 1:
                    self.current_bbox.y0 -= CFG['ASPECT_STEP']
                else:
                    self.current_bbox.y1 -= CFG['ASPECT_STEP']
            elif direction == 'down':
                if grow == 1:
                    self.current_bbox.y1 += CFG['ASPECT_STEP']
                else:
                    self.current_bbox.y0 += CFG['ASPECT_STEP']
            elif direction == 'left':
                if grow == 1:
                    self.current_bbox.x0 -= CFG['ASPECT_STEP']
                else:
                    self.current_bbox.x1 -= CFG['ASPECT_STEP']
            elif direction == 'right':
                if grow == 1:
                    self.current_bbox.x1 += CFG['ASPECT_STEP']
                else:
                    self.current_bbox.x0 += CFG['ASPECT_STEP']
            self._draw_bbox()

    def _rotate_bbox(self, e, dtheta):
        if len(self.mouse_poses) == 4:
            if dtheta == 0:
                if e.delta > 0:
                    self.current_bbox.theta -= CFG['ROTATE_STEP']
                else:
                    self.current_bbox.theta += CFG['ROTATE_STEP']
            else:
                self.current_bbox.theta += dtheta
            self._draw_bbox()


    def _shift_mouse(self, e):
        print e.__dict__
            
