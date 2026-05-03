include <BOSL/constants.scad>
use <BOSL/shapes.scad>
use <BOSL/transforms.scad>

include <extra/colorset.scad>

/* //ColourWheel
CWh=[
    [0,"Fuchsia"],
    [1,"DarkCyan"],
    [2,"lime"],
    [3,"DodgerBlue"],
    [4,"greenyellow"],
    [5,"yellow"],
    [6,"LightCoral"],
    [7,"red"],
    [8,"SandyBrown"],
    [9,"Goldenrod"],
    [10,"DarkGoldenrod"],
    [11,"SlateGray"] 
    ]; */

//---Prod Values---
//CubeFillet=0.5;

//---Dev Values---
CubeFillet=0;
BaseCntr = false;
$fn=100;
//Offsets to match the current Cyberdeck copying
COSetY=6.3; OffsetBazFz=5;

//Original Cyberdeck STL Imported
translate([50,COSetY,0]) color(CWh[0][1]) import("cyberdeck-Body.stl");
translate([120,COSetY,0]) color(CWh[0][1]) import("cyberdeck-Body.stl");
//color(CWh[0][1]) import("cyberdeck-topPanelRight.stl");


//Offset Function
function  oset (base, sec) =  (base - sec) / 2;

//Creating a base traingle and moving it to the an xyz positive postion
module BaseTri (TX,TY,TZ,COSetY) {
    color(CWh[3][1])
    translate([TX/2,COSetY+(TY/2),0])
    right_triangle([TX,TY,TZ], align=V_UP+V_BACK+V_RIGHT, orient=ORIENT_X, center=BaseCntr);
}

//Picatinny Rails Triangles
module PicRailTri(Ax, TBy, TBz){
    translate([0,TBz,TBz]) rotate(a=180, v=[1,0,0]) union(){
    BaseTri(Ax,TBy/2,TBz,0);
    mirror([0,90,0]) BaseTri(Ax,TBy/2,TBz,0);}
}

module PicRails(){
    PAz=15.67; CPADiffy=7.45;
    TBy=5.53; TBz=2.8;
    //Rial Distance
    PRailThick=4.75; PRailDist=5.25;
    difference(){
    union(){
    translate([0,0,OffCz+CPADiffy]) cuboid ([Ax,TBy+1,PAz], fillet=CubeFillet,center=BaseCntr);
    translate([0,0,(OffCz+CPADiffy-TBz)]) PicRailTri(Ax,TBy,TBz);
    translate([0,0,(OffCz+CPADiffy+PAz+TBz)]) mirror([0,0,90]) PicRailTri(Ax,TBy,TBz);
    }
        for (Movx=[PRailThick:PRailThick+PRailDist:Ax]) {translate([Movx,0,OffCz+CPADiffy-TBz]) #cuboid ([PRailThick,TBy/2,PAz+(2*TBz)], fillet=CubeFillet,center=BaseCntr);}
    }
}

//---Bottom Layer---
//Base Cubiod Dimensions
Ax=60; Ay=170; Az=14;
//Second Layer Cuboid Dimensions
Bx=Ax; By=146; Bz=9;
difference(){
    //Base Cuboid
    translate([0,COSetY,0]) cuboid ([Ax,Ay,Az], fillet=CubeFillet,center=BaseCntr);
    //Second Layer Cuboid
    translate([0,COSetY+oset(Ay,By),OffsetBazFz]) cuboid ([Bx,By,Bz], fillet=CubeFillet,center=BaseCntr);
    //Base Triangle Dimensions
    TAx=60; TAy=10; TAz = 10;
    //First Triangle
    BaseTri(TAx,TAy,TAz,COSetY);
    //Second Triangle
    translate ([0,COSetY+Ay,0]) mirror([0,90,0]) BaseTri(TAx,TAy,TAz,0);

}
CAh=1; CAr=3; Count=1;
//54 Difference 49
CAyOne=35; CayTwo=CAyOne+58; CayThr=CayTwo+47;
for (CAMovx=[5:49:Ax]){
    translate([CAMovx,CAyOne+COSetY,0]) #cylinder(h=CAh, r1=CAr, r2=CAr, center=true);
    translate([CAMovx,CayTwo+COSetY,0]) #cylinder(h=CAh, r1=CAr, r2=CAr, center=true);
    translate([CAMovx,CayThr+COSetY,0]) #cylinder(h=CAh, r1=CAr, r2=CAr, center=true);
    if (CAMovx+24.5 < Ax) {
        translate([CAMovx+24.5,(CAyOne+CayTwo)/2+COSetY/2,0]) #cylinder(h=CAh, r1=CAr, r2=CAr, center=true);
        translate([CAMovx+24.5,(CayTwo+CayThr)/2+COSetY/2,0]) #cylinder(h=CAh, r1=CAr, r2=CAr, center=true);

    }
}
SLAl=Ax; SLAr1=5; SLAr2=3; SLAh=2;
translate([SLAl/2+SLAr1,0,0]) rotate([30,0,0]) slot(l=45, r1=SLAr1, r2=SLAr2, h=SLAh);


//---Middle Layer---
//Third Layer Cuboid Dimensions Cy=182;
Cx=Ax; Cy=182.6-(2*(COSetY)); Cz=30; OffCz=Az; CDDiffy=5;
//Fourth Layer Cuboid Dimensions Dy=Cy-(2*(COSetY+5));
Dx=Ax; Dy=Cy-(2*CDDiffy); Dz=Cz;
difference(){
    //Base
    translate([0,COSetY,OffCz]) cuboid ([Cx,Cy,Cz], fillet=CubeFillet,center=BaseCntr);
    //Removde Cube Middle
    translate([0,COSetY+CDDiffy,OffCz]) cuboid ([Dx+1,Dy,Dz], fillet=CubeFillet,center=BaseCntr);
    //translate([0,0,OffCz]) cuboid ([Cx,7,4.7], fillet=CubeFillet,center=BaseCntr);
    //translate([0,5.6,OffCz+4.7]) cuboid ([Cx,0.7,2.8], fillet=CubeFillet,center=BaseCntr);
}
PicRails();
translate([0,2*(COSetY)+Cy,0]) mirror([0,90,0]) PicRails();
//TBy=6.3; TBz=4;
//translate([Ax/2,TBz/2+1,21.5]) rotate(a=180, v=[1,1,0]) prismoid(size1=[TBy-0.7,Ax], size2=[0,Ax], h=TBz, align=V_UP+V_BACK+V_RIGHT, center=BaseCntr);

//---Top Layer---
//Fifth Layer Cuboid Dimensions
Ex=Ax; Ey=Cy; Ez=11; OffEz=Az+Cz; EFDiffy=12; EGDiffy=CDDiffy;
Fy=Cy-(2*EFDiffy); Fz=8;
Gy=Dy; Gz=3;

difference(){
    //Initial Cube that covers entire area that will be cut from
    translate([0,COSetY,OffEz]) cuboid ([Ex,Ey,Ez], fillet=CubeFillet,center=BaseCntr);
    //Bottom Layer of Cuboid cut from above
    translate([0,COSetY+EFDiffy,OffEz]) color(CWh[6][1]) cuboid ([Ex+1,Fy,Fz], fillet=CubeFillet,center=BaseCntr);
    //Top Layer of Cuboid cut from above
    translate([0,COSetY+EGDiffy,OffEz+Fz]) color(CWh[3][1]) cuboid ([Ex+1,Gy,Gz], fillet=CubeFillet,center=BaseCntr);
    //Two top corner traingles
    translate([0,COSetY,OffEz+Fz+Gz]) mirror([0,0,90]) BaseTri(Ex,5,5,0);
    translate([0,COSetY+Ey,OffEz+Fz+Gz]) mirror([0,90,90]) BaseTri(Ex,5,5,0);
    CAh=Fz; CAr=2;
    translate([Ex/2,CAr+EFDiffy+0.85,OffEz+4]) cylinder(h=CAh, r1=CAr, r2=CAr, center=true);
    translate([Ex/2,CAr+Gy+5.75,OffEz+4]) cylinder(h=CAh, r1=CAr, r2=CAr, center=true);
}

