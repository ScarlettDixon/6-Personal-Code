include <BOSL/constants.scad>
use <BOSL/shapes.scad>

//Test

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
BaseX = 40;
BaseY = 55;
BaseZ = 3;
BaseCntr = false;

//Offset Function
function  oset (base, sec) =  (base - sec) / 2;

//KeyStone Jack Hole Dimensions
KHAx = 15; KHAz = 20;
//Crossbar Thickness
CT=5;
//Extrude Value
EV=2;
//Text Size
TS=2;
//Keystone Faceplate
Kx = 115; Ky = 1.5; Kz = (2*KHAz)+(3*CT);

//Thickness
Thickness=[1.3,1.4,1.5,1.6,1.7];
KeyHeight=[19.3,19.4,19.5,19.6,19.7];


difference(){
    for (Movx=[0:1:4]){
        translate([Movx*(KHAx+(2*CT)),0,0]) color(CWh[Movx][1]) cuboid([KHAx+(2*CT),Thickness[Movx],Kz], fillet=0,center=BaseCntr);
    }
    for (Movx=[0:1:4]){
        translate([5+(10*Movx)+(KHAx*Movx),0,5]) #cuboid([KHAx,Thickness[Movx],KeyHeight[Movx]],center=BaseCntr);
        translate([(KHAx)/2+(Movx*(KHAx+(2*CT))),1.5,1]) rotate([90,0,0]) linear_extrude(EV) text( text=str(KeyHeight[Movx]), size=TS);
        translate([(KHAx)/2+(Movx*(KHAx+(2*CT))),1.5,1+KHAz+CT]) rotate([90,0,0]) linear_extrude(EV) text( text=str(KeyHeight[Movx]), size=TS);
        translate([(KHAx)/2+(Movx*(KHAx+(2*CT))),1.5,1+2*(KHAz+CT)]) rotate([90,0,0]) linear_extrude(EV) text( text=str(Thickness[Movx]), size=TS);
        translate([5+(10*Movx)+(KHAx*Movx),0,10+KHAz]) #cuboid([KHAx,Thickness[Movx],KeyHeight[Movx]],center=BaseCntr);
    }
}
    // for (Movz=[CT:KHAz+CT:Kz-CT]){
    // for (Movx=[(2*CT):KHAx+CT:Kx-(KHAx+(2*CT))]){
    //     translate([Movx,-1,Movz]) #cuboid([KHAx,Ky+2,KHAz],center=BaseCntr);
    // }
    // }
    //translate([oset(Kx, KHAx),-1,oset(Kz, KHAz)]) #cuboid([KHAx,Ky+2,KHAz],center=BaseCntr);
