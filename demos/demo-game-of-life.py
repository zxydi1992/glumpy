#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Copyright (C) 2009-2010  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------
import numpy, glumpy
import OpenGL.GL as gl

n = 512
Z = numpy.random.randint(0,2,(n,n)).astype(numpy.float32)
window = glumpy.Window(512, 512)
viewport = [0,0,1]
Zi = glumpy.Image(Z, interpolation='nearest', cmap=glumpy.colormap.Grey,
                  vmin=1, vmax=0)
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

@window.event
def on_mouse_motion(x, y, dx, dy):
    zoom = viewport[2]
    x = x/float(window.width)
    y = y/float(window.height)
    x = min(max(x,0),1)
    y = min(max(y,0),1)
    viewport[0] = x*window.width*(1-zoom)
    viewport[1] = y*window.height*(1-zoom)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    zoom = viewport[2]
    if scroll_y > 0:
        zoom *= 1.25
    elif scroll_y < 0:
        zoom /= 1.25
    viewport[2] = min(max(zoom,1),20)
    on_mouse_motion(x,y,0,0)

@window.event
def on_draw():
    window.clear()
    x,y,s = viewport
    Zi.blit(x, y, s*window.width, s*window.height)

@window.event
def on_idle(dt):
    # Code by Tom Wright
    # http://tat.wright.name/game-of-life/game-of-life.py
    N = numpy.zeros(Z.shape)
    N[1:, 1:] += Z[:-1, :-1]
    N[1:, :-1] += Z[:-1, 1:]
    N[:-1, 1:] += Z[1:, :-1]
    N[:-1, :-1] += Z[1:, 1:]
    N[:-1, :] += Z[1:, :]
    N[1:, :] += Z[:-1, :]
    N[:, :-1] += Z[:, 1:]
    N[:, 1:] += Z[:, :-1]
    Z[...] = ((Z == 1) & (N < 4) & (N > 1)) | ((Z == 0) & (N == 3))
    Zi.update()
    window.draw()

window.mainloop()
