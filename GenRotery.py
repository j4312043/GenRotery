'''
Created on 2022/07/02

@author: Fumiya
'''
import getopt
import sys
import sdxf
import math
import numpy

def calcX(rc , rm , e , R , theta):
    return (rm - rc) * math.cos(theta) + R * math.cos((1 - rc / rm)*theta)

def calcY(rc , rm , e , R , theta):
    return (rm - rc) * math.sin(theta) + R * math.sin((1 - rc / rm)*theta)

#x,y座標の配列をつなげる(最初と最後もつなげる
def DrawOuter(dxf,x,y,layer_name):
    for i in range(1,len(x)):
        dxf.append( sdxf.Line(points=[(x[i-1],y[i-1]),  (x[i],y[i])], layer=layer_name ) )
    dxf.append( sdxf.Line(points=[(x[-1],y[-1]),  (x[0],y[0])], layer=layer_name) )
    return


'''
Main proc
'''
#parameter
# ここの4つの変数を設定する。
rc = 8
rm = rc*3/2
R = 30
e = rm-rc

dxf_housing=sdxf.Drawing()
dxf_housing.layers.append(sdxf.Layer(name="layer1", color=1) )    #yellow text layer

#ハウジング形計算の計算
x=[]
y=[]
x.append( calcX(rc , rm , e , R , 0) )
y.append( calcY(rc , rm , e , R , 0) )
for theta in numpy.arange(0,3* 2*math.pi , 0.1):
    x.append( calcX(rc , rm , e , R , theta) )
    y.append( calcY(rc , rm , e , R , theta) )
DrawOuter(dxf_housing,x,y,"layer1")
dxf_housing.append( sdxf.Circle(center=(0, 0), radius=2, layer="layer1") )


dxf_rotar=sdxf.Drawing()
dxf_rotar.layers.append(sdxf.Layer(name="layer1", color=1) )
#ロータ側計算
# 第三引数で分解能を指定できる
for theta_d in numpy.arange(0, 2*math.pi , 0.2):
    rotar_x = []
    rotar_y = []

    for i in range( len(x) ):
        rotar_x.append( e*math.cos(theta_d) + x[i]*math.cos(theta_d/2) + y[i]*math.sin(theta_d/2) )
        rotar_y.append( e*math.sin(theta_d) - x[i]*math.sin(theta_d/2) + y[i]*math.cos(theta_d/2) )

    DrawOuter(dxf_rotar,rotar_x,rotar_y,"layer1")

dxf_rotar.append( sdxf.Circle(center=(0, 0), radius=2, layer="layer1") )

try:
    dxf_housing.saveas("housing.dxf")
    dxf_rotar.saveas("rotary.dxf")
except:
    print("Problem saving file")
    sys.exit(2)

if __name__ == '__main__':
    print("Gen Rotery DXF")
    pass