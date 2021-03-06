# generated by 'clang2py'
# flags '-c -k cdefmstu -o message_defs.py message_defs.h'
# -*- coding: utf-8 -*-
#
# TARGET arch is: []
# WORD_SIZE is: 4
# POINTER_SIZE is: 8
# LONGDOUBLE_SIZE is: 8
#
import ctypes




MT_REQUEST_TEST_DATA = 101 # macro
MT_TEST_DATA = 102 # macro
MT_GO_L = 103 # macro
MT_GO_R = 104 # macro
class struct_c__SA_MDF_TEST_DATA(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('a', ctypes.c_int32),
    ('b', ctypes.c_int32),
    ('x', ctypes.c_double),
     ]

MDF_TEST_DATA = struct_c__SA_MDF_TEST_DATA
class struct_c__SA_MDF_GO_L(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pressedL', ctypes.c_int16),
     ]

MDF_GO_L = struct_c__SA_MDF_GO_L
class struct_c__SA_MDF_GO_R(ctypes.Structure):
    _pack_ = True # source:False
    _fields_ = [
    ('pressedR', ctypes.c_int16),
     ]

MDF_GO_R = struct_c__SA_MDF_GO_R
__all__ = \
    ['MDF_GO_L', 'MDF_GO_R', 'MDF_TEST_DATA', 'MT_GO_L', 'MT_GO_R',
    'MT_REQUEST_TEST_DATA', 'MT_TEST_DATA', 'struct_c__SA_MDF_GO_L',
    'struct_c__SA_MDF_GO_R', 'struct_c__SA_MDF_TEST_DATA']
