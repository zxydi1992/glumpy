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
''' Various shaders for texture processing.

    Shaders are used to program the graphics processing unit (GPU) programmable
    rendering pipeline, which has mostly superseded the fixed-function pipeline
    that allowed only common geometry transformation and pixel shading
    functions; with shaders, customized effects can be used.

    Vertex shaders are run once for each vertex given to the graphics
    processor. The purpose is to transform each vertex's 3D position in virtual
    space to the 2D coordinate at which it appears on the screen (as well as a
    depth value for the Z-buffer). Vertex shaders can manipulate properties such
    as position, color, and texture coordinate, but cannot create new
    vertices. The output of the vertex shader goes to the next stage in the
    pipeline, which is either a geometry shader if present or the rasterizer
    otherwise.

    Geometry shaders can add and remove vertices from a mesh. Geometry shaders
    can be used to generate geometry procedurally or to add volumetric detail to
    existing meshes that would be too costly to process on the CPU. If geometry
    shaders are being used, the output is then sent to the rasterizer.

    Pixel shaders, also known as fragment shaders, calculate the color of
    individual pixels. The input to this stage comes from the rasterizer, which
    fills in the polygons being sent through the graphics pipeline.  Pixel
    shaders are typically used for scene lighting and related effects such as
    bump mapping and color toning.  (Direct3D uses the term "pixel shader,"
    while OpenGL uses the term "fragment shader." The latter is arguably more
    correct, as there is not a one-to-one relationship between calls to the
    pixel shader and pixels on the screen. The most common reason for this is
    that pixel shaders are often called many times per pixel for every object
    that is in the corresponding space, even if it is occluded; the Z-buffer
    sorts this out later.)
'''
from shader import Shader
from nearest import Nearest
from bilinear import Bilinear
from bicubic import Bicubic
