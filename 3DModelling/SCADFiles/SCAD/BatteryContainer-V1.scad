include <BOSL2/std.scad>
include <BOSL2/walls.scad>
use <BOSL/shapes.scad>
use <BOSL/transforms.scad>
use <threads-scad/threads.scad>
use <extra/hex-grid.scad>

//ColourWheel
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
    ];


$fn=100;
//Offset Function
function  oset (base, sec) =  (base - sec) / 2;

//Battery Pack Dimensions
IntX = 71; IntY = 157; IntZ = 42;
Thickness=3; //Outer Edge
Ofs=0.4; HOfs=Ofs/2;
//Outer Dimensions
OutX=IntX+(2*Ofs)+(2*Thickness); OutY=IntY+(2*Ofs)+(2*Thickness); OutZ = IntZ+(2*Ofs)+(2*Thickness);
//Front Plate Cutout Dimensions
FPCx=62+(2*Ofs); FPCz=15+(2*Ofs); FPCFlt=5;

BaseCntr = false;
difference(){union(){
//Left Outer Wall
color(CWh[2][1]) y_grid(size=[Thickness,OutY,OutZ],SW=10,wall=3);
//translate([Thickness/2,OutY/2,OutZ/2]) rotate([0,90,0]) color(CWh[2][1]) create_grid(size=[OutZ,OutY,Thickness],SW=10,wall=3);
//sparse_strut(h=OutZ, l=OutY, thick=Thickness, strut=6, align=RIGHT+UP+BACK);
//Front Plate
cuboid([OutX,Thickness,OutZ],rounding=0,p1=[0,0,0]);
//Right Outer Wall
translate([OutX-Thickness,0,0]) color(CWh[2][1]) y_grid(size=[Thickness,OutY,OutZ],SW=10,wall=3);
//translate([OutX-Thickness,0,0]) translate([Thickness/2,OutY/2,OutZ/2]) rotate([0,90,0]) color(CWh[2][1]) create_grid(size=[OutZ,OutY,Thickness],SW=10,wall=3);
//translate([OutX-Thickness,0,0]) sparse_strut(h=OutZ, l=OutY, thick=Thickness, strut=6, align=RIGHT+UP+BACK);
//Back Plate
//translate([0,OutY-Thickness,0])cuboid([OutX,Thickness,OutZ],rounding=0,center=BaseCntr);
//Bottom Outer Wall
//translate([0,0,Thickness]) rotate([0,90,0]) sparse_strut(h=OutX, l=OutY, thick=Thickness, strut=6, align=RIGHT+UP+BACK);
translate([0,0,Thickness]) rotate([0,90,0]) sparse_wall(h=OutX, l=OutY, thick=Thickness, strut=6, anchor=[-1,-1,-1]);
//Top Outer Wall
translate([0,0,OutZ]) rotate([0,90,0]) sparse_strut(h=OutX, l=OutY, thick=Thickness, strut=6, align=[1,1,1]);
}
//difference(){
//translate([oset(OutX,0),0,oset(OutZ,0)]) #sparse_strut3d(w=OutX, l=OutY, h=OutZ, align=ALIGN_POS);
//translate([Thickness,Thickness,Thickness]) #cuboid([IntX,IntY,IntZ],rounding=0.5,center=BaseCntr);
//Removal of the Backend
//#cuboid([OutX+HOfs,OutY,OutZ+HOfs],rounding=0,p1=[0,10,0]);
//Front Plate Cutout
#cuboid([FPCx,Thickness+20,FPCz],rounding=FPCFlt, p1=[Thickness+oset(IntX,FPCx),-5,Thickness+oset(IntZ,FPCz)]);
//translate([Thickness+oset(IntX,FPCx),-5,Thickness++oset(IntZ,FPCz)]) #cuboid([FPCx,Thickness+20,FPCz],rounding=0,center=BaseCntr);
}
//create_grid(size=[100,150,10],SW=20,wall=4);

