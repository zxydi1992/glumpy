#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# glumpy - Fast OpenGL numpy visualization
# Copyright (c) 2009 - Nicolas P. Rougier
#
# This file is part of glumpy.
#
# glumpy is free  software: you can redistribute it and/or  modify it under the
# terms of  the GNU General  Public License as  published by the  Free Software
# Foundation, either  version 3 of the  License, or (at your  option) any later
# version.
#
# glumpy is  distributed in the  hope that it  will be useful, but  WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy  of the GNU General Public License along with
# glumpy. If not, see <http://www.gnu.org/licenses/>.
#
# -----------------------------------------------------------------------------
import pyglet
pyglet.options['debug_gl'] = False
import pyglet.gl as gl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import glumpy


transparent = np.array([1,2,3,255])
items = []

def imshow(X, cmap=None, norm=None, aspect=None, interpolation=None,
           alpha=1.0, vmin=None, vmax=None, origin=None, extent=None,
           **kwargs):

    '''pylab imshow proxy function.

       This function first call the pylab original imshow function using an
       alpha level of 0 (fully transparent). It then set axes background with a
       dedicated 'transparent' color that will be replaced later by a truly
       transparent color.

       Warning: any pixel with 'transparent' color will be replaced by a
                transparent pixel. If this causes problem, you will have to
                change the definition of 'transparent' to something else.
    '''
    axis = plt.imshow(X, cmap=cmap, norm=norm, aspect=aspect,
                      interpolation='nearest', alpha=0, vmin=vmin,
                      vmax=vmax, origin=origin, extent=extent, **kwargs)
    r,g,b,a = transparent/255.0
    cmap = axis.cmap
    under = cmap(-1.0)
    over = cmap(2.0)
    axis.cmap.set_over((r,g,b), alpha=0)
    axis.cmap.set_under((r,g,b), alpha=0)
    axis.cmap.set_bad((r,g,b), alpha=0)
    axes = axis.get_axes()
    axes.patch.set_facecolor((r,g,b))
    axes.patch.set_alpha(a)
    # Build glumpy colormap from matplotlib colormap
    colors=[]
    for i in range(510):
        colors.append((i/510.0, cmap(i/510.0, alpha=alpha)))
    cmap = glumpy.colormap.Colormap(*colors, over=glumpy.Color(over), under=glumpy.Color(under))
    #cmap.set_alpha(alpha)
    image = glumpy.Image(X,interpolation=interpolation, cmap=cmap, vmin=vmin, vmax=vmax)
    image.update()
    items.append ([image,axis,alpha])
    return axis


def show(interpolation='nearest'):
    ''' pylab show proxy function. '''

    # Draw current figure to rgba buffer
    fig = plt.gcf()
    fig.canvas.draw()
    buffer = fig.canvas.buffer_rgba(0,0)
    x,y,w,h = fig.bbox.bounds
    F = np.fromstring(buffer,np.uint8)
    F.shape = h,w,4

    # Replace 'transparent' color with a real transparent color
    v = np.array(transparent,dtype=np.uint8).view(dtype=np.int32)[0]
    Ft = np.where(F.view(dtype=np.int32) == v, 0, F)

    # Create main frame 
    frame = glumpy.Image(Ft,interpolation=interpolation)
    frame.update()

    window = pyglet.window.Window(frame.shape[1], frame.shape[0],
                                  vsync=0, resizable=True)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    fps_display = pyglet.clock.ClockDisplay()

    @window.event
    def on_draw():
        window.clear()
        for image,axis,alpha in items:
            x,y,w,h = axis.get_axes().bbox.bounds
            x /= float(frame.shape[1])
            y /= float(frame.shape[0])
            w /= float(frame.shape[1])
            h /= float(frame.shape[0])
            gl.glColor4f(1,1,1,alpha)
            image.blit(x*window.width,y*window.height,
                       w*window.width,h*window.height)
        gl.glColor4f(1,1,1,1)
        frame.blit(0,0,window.width, window.height)
        fps_display.draw()

    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            if window.width == frame.shape[1] and window.height == frame.shape[0]:
                pyglet.app.exit()
            else:
                window.set_size(frame.shape[1], frame.shape[0])
            return True
    pyglet.app.run()


def func3(x,y):
    return (1- x/2 + x**5 + y**3)*np.exp(-x**2-y**2)
dx, dy = 0.05, 0.05
x = np.arange(-3.0, 3.0, dx, dtype=np.float32)
y = np.arange(-3.0, 3.0, dy, dtype=np.float32)
X,Y = np.meshgrid(x, y)


xmin, xmax, ymin, ymax = np.amin(x), np.amax(x), np.amin(y), np.amax(y)
extent = xmin, xmax, ymin, ymax
fig = plt.figure()
Z1 = np.array(([0,1]*4 + [1,0]*4)*4, dtype=np.float32)
Z1.shape = 8,8  # chessboard
im1 = imshow(Z1, cmap=plt.cm.gray, interpolation='nearest', extent=extent)
#plt.hold(True)
Z2 = func3(X, Y)
im2 = imshow(Z2, cmap=plt.cm.jet, alpha=.9, interpolation='bilinear',  extent=extent)
#axis([xmin, xmax, ymin, ymax])
show()
