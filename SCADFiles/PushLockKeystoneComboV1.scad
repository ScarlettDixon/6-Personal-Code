include <BOSL/constants.scad>
use <BOSL/shapes.scad>

//Test

$fn=100;
BaseX = 40;
BaseY = 55;
BaseZ = 3;
BaseCntr = false;

union(){
color("Lime", 1.0){
difference(){
    //Base
    cuboid([BaseX,BaseY,BaseZ] , fillet=0.5,center=BaseCntr);
    //Holes
    for (x = [5:30:35]) {
        for (y = [16:24:40]){
            translate([x,y,-1]){
                cylinder(BaseZ+2,3,3);
            }
        }
    }
}
}
}

//Offset Function
function  oset (base, sec) =  (base - sec) / 2;

//Keystone Faceplate
KeyY = 1; KeyZ = 30;
KeyHolX = 15 ; KeyHolZ = 20 ;
translate([0,0,BaseZ]){
    color("Aqua", 1.0){
    difference(){
        cuboid([BaseX,KeyY,KeyZ], fillet=0.5,center=BaseCntr);
        translate([oset(BaseX, KeyHolX),-1,oset(KeyZ, KeyHolZ)]){
            cuboid([KeyHolX,KeyY+2,KeyHolZ],center=BaseCntr);
        }
    }
}

//Keystone Internals
KeyIntX = 20; KeyIntY=18;
KeyIntHolX = 15;  KeyIntHolZ = (KeyZ-2);
    
    translate([oset(BaseX, KeyIntX),1,0]){
        difference(){
        cuboid([KeyIntX,KeyIntY,KeyZ], fillet=0.5,center=BaseCntr);
        translate ([oset(KeyIntX, KeyIntHolX),0,0]){
        cuboid([KeyIntHolX,KeyIntY+1,KeyIntHolZ],center=BaseCntr);
        }
    }
}
//Keystone Baseplate
    
}