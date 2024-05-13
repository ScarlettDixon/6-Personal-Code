include <BOSL/constants.scad>
use <BOSL/shapes.scad>
use <BOSL/transforms.scad>
include <BOSL2/std.scad>
include <BOSL2/walls.scad>

include <extra/colorset.scad>


//---Dev Values---
CubeFillet=0;
BaseCntr = false;
$fn=100;
//Offsets to match the current Cyberdeck copying
COSetY=6.3; OffsetBazFz=5;

//---Bottom Layer---
//Base Cubiod Dimensions
BAx=45; BAy=170; BAz=5;
//Second Layer Cuboid Dimensions
BBx=BAx; BBy=12; BBz=9;

//Base Triangle Dimensions
TAx=BAx; TAy=10; TAz = 10;

//Creating a base traingle and moving it to the an xyz positive postion
module BaseTri (TX,TY,TZ,COSetY) {
    color(CWh[3][1])
    translate([TX/2,COSetY+(TY/2),0])
    right_triangle([TX,TY,TZ], align=V_UP+V_BACK+V_RIGHT, orient=ORIENT_X, center=BaseCntr);
}


difference(){ union() {
color(CWh[60][1]) cuboid([BAx,BAy,BAz],rounding=0,p1=[0,COSetY,0]);
color(CWh[65][1]) cuboid([BBx,BBy,BBz],rounding=0,p1=[0,COSetY,BAz]);
color(CWh[65][1]) cuboid([BBx,BBy,BBz],rounding=0,p1=[0,COSetY+BAy-BBy,BAz]);
}
    //First Triangle
    BaseTri(TAx,TAy,TAz,COSetY);
    //Second Triangle
    translate ([0,COSetY+Ay,0]) mirror([0,90,0]) BaseTri(TAx,TAy,TAz,0);
}
translate([225,COSetY,0]) color(CWh[0][1]) import("cyberdeck-endCap.stl");