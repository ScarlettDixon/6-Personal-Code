use <BOSL2/std.scad>
use <extra/keystone-jack-pieces.scad>
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


//Offset Function
function  oset (base, sec) =  (base - sec) / 2;
//Combine parts offset
CPO=0.5;


//---KEYSTONE PANEL VALUES---
//Matrix - Columns and Rows - Change here for different design
Colsx = 5;
Rowsz = 2;
//Crossbar Thickness - Distance between the crossbars in the middle
CT=5; 
//Edge Thickness - The Thickness of the outer edge to the left and right
ET=10;
//KeyStone Jack Hole Dimensions
KHAx = 15; KHAz = 19.7;
//Keystone Faceplate
Kx = (Colsx * KHAx) + (2 * ET) + ((Colsx-1)*CT); Ky = 1.5; Kz = (Rowsz*KHAz)+((Rowsz+1)*CT);

//---KEYSTONE PANEL HOLDER VALUES---
// Keystone Panel Slot dimensions
SAx=2; SAy=2.5;
//Base Plate Dimension
BPAx=Kx+(2*SAx); BPAy=40; BPAz=3;
//First Outer Pillar Dimensions - Front Container for Slot
PAx=ET+SAx; PAy=8;
//Second Outer Pillar Dimensions - Slot
PBx=SAx; PBy=SAy;
//Third Outer Pillar Dimensions - Back Container for Slot
OPCover=3; OPCx=PAx-SAx; OPCy=PAy+13; OPCSlots=3; OPCThickness=(OPCx-OPCSlots)/2;
//Inner Pillar Dimensions
PCx=5; PCy=PAy;
//Crossbar Dimensions
CRAx=BPAx; CRAy=2; CRBy=3; CRAz=CT;
//Extra On top for removal
EBAz=5;

//---KEYSONE BACK PANEL VALUES---
//Slot Dimensions
SLAx=3; SLAy=PAy; SLAz=3;


difference() { union(){
//Base
color(CWh[0][1]) x_grid([BPAx,BPAy,BPAz], 5,2);
//color(CWh[0][1]) cuboid([BPAx,BPAy,BPAz], rounding=0,p1=[0,0,0]);
for (LR=[0:1:1]){
        //Outer Pillars First Layer - Front wall
        color(CWh[1][1]) cuboid([PAx,PAy,Kz+EBAz], rounding=0,p1=[LR*(BPAx-PAx),0,BPAz]);
        //Outer Pillars Second Layer - Slots Covered
        color(CWh[3][1]) cuboid([PBx,PBy,Kz+EBAz], rounding=0,p1=[LR*(BPAx-PBx),PAy,BPAz]);
        color(CWh[7][1]) cuboid([OPCx,SAy,EBAz-SAy], rounding=0,p1=[PBx+LR*(BPAx-(OPCx+2*(PBx))),PAy,BPAz+Kz+EBAz-SAy]);
        //Outer Pillars Second Layer - Slots Uncovered
        color(CWh[5][1]) cuboid([PBx,PBy,Kz+EBAz], rounding=0,p1=[LR*(BPAx-PBx),PAy+PBy,BPAz]);
        //Outer Pillars Third Layer
        //color(CWh[4][1]) cuboid([OPCx,OPCy,Kz+EBAz], rounding=0,p1=[LR*(BPAx-OPCx),PAy+(2*PBy),BPAz]);
        //Outer Pillars Third Layer - 1
        color(CWh[6][1]) translate([LR*(BPAx-OPCThickness),PAy+(2*PBy),BPAz]) y_grid([OPCThickness, OPCy, Kz+EBAz],4,1);
        color(CWh[4][1]) cuboid([OPCSlots,OPCy-OPCSlots,Kz+EBAz-OPCSlots], rounding=0,p1=[OPCThickness+(LR*(BPAx-OPCx)),PAy+(2*PBy),BPAz]);
        color(CWh[6][1]) translate([OPCThickness+OPCSlots+(LR*(BPAx-(2*(OPCThickness)+3*(OPCSlots)))),PAy+(2*PBy),BPAz]) y_grid([OPCThickness, OPCy, Kz+EBAz],4,1);
    }
//Inner Pillars
for (movINPA=[1:1:Colsx-1]){
    color(CWh[movINPA][1]) cuboid([PCx,PCy,Kz], rounding=0,p1=[PAx+(movINPA*KHAx)+((movINPA-1)*PCx),0,BPAz]);
}

//Support Crossbar
CTB=8;
for (movCRA=[0:1:Rowsz]){
    cuboid([CRAx,CRAy,CTB], rounding=0,p1=[0,0,(movCRA*CTB)+(movCRA*17)]);
}

}
//---DIFFERENCE BEGINS HERE---
CTC=CT-2;
for (LRB=[0:1:1]){
    //Slots to remove from top of third pillar - Y Direction
    //color(CWh[5][1]) #cuboid([SLAx,BPAy,SLAz], rounding=0,p1=[(oset(OPCx,SLAx)+(LRB*(BPAx-OPCx))),2,(BPAz+Kz+EBAz)-SLAz]);
    //Slots to remove from back of third pillar - Z Direction
    //color(CWh[5][1]) #cuboid([SLAx,SLAz,Kz+SLAz], rounding=0,p1=[(oset(OPCx,SLAx)+(LRB*(BPAx-OPCx))),PAy+(2*PBy)+OPCy-SLAz,BPAz]);
    //Internal Crossbar slots for back panel - Y Direction
    
    for (movCRSL=[0:1:Rowsz]){
        #cuboid([((OPCx-SLAx)/2)+SLAx,BPAy,CTC], rounding=1,p1=[OPCx-((OPCx-SLAx)/2) +(LRB*(BPAx-(OPCx+SLAx+((OPCx-SLAx)/2)+SLAx))),PAy,BPAz+(movCRSL*KHAz)+(movCRSL*CT)+oset(CT,CTC)]);
    }
}

}
//translate([0,PAy,BPAz]) KeystonePanel(5,2,10,5,5);

/* for (x = [PAx+KHAx:PCx+KHAx:Kx-PAx]) {
    color(CWh[2][1]) cuboid([PCx,PCy,PCz], rounding=0,p1=[x,0,BPAz]);
} */

//Faceplate Covers Dimensions
// FPAx=Kx; FPAy=1; FPAz=Kz;
//translate([0,28,BPAz]) cuboid([CRAx,CRBy,CRAz], rounding=0,p1=false);
//translate([PAx,0,BPAz]) color(CWh[2][1]) cuboid([FPAx,FPAy,FPAz], rounding=0,p1=false);

//Internal Crossbar slots for back panel - Y Direction

/* for (movCRSL=[0:1:Rowsz]){
    #cuboid([2*(SLAx),BPAy,CTC], rounding=0,p1=[OPCx-SLAx,CRAy,BPAz+(movCRSL*KHAz)+(movCRSL*CT)+oset(CT,CTC)]);
    #cuboid([2*(SLAx),BPAy,CTC], rounding=0,p1=[BPAx-(OPCx+SLAx),CRAy,BPAz+(movCRSL*KHAz)+(movCRSL*CT)+oset(CT,CTC)]);
} */