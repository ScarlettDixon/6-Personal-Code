use <BOSL2/std.scad>
// The Belfry OpenSCAD Library V2
// Source: https://github.com/revarbat/BOSL2
// Documentation: https://github.com/revarbat/BOSL2/wiki
// BOSL2 is licensed under BSD 2-Clause License
//    https://github.com/revarbat/BOSL2/blob/master/LICENSE

$fn=100;

//Offset Function
function  oset (base, sec) =  (base - sec) / 2;

////////////////////////////////////////////////////////////////////
// KeystonePanel: Takes initial parameters to design an initial panel for use with the keystone holder.
//
//  Colsx: Number of Keystone hole columns.
//  Rowsz: Number of Keystone hole rows.
//  ETx: The outer edge thickness in the X direction. Top and Bottom.
//  ETz: The outer edge thickness in the Z direction. Left and Right.
//  CT: Internal Crossbar Thickness
////////////////////////////////////////////////////////////////////
module KeystonePanel(Colsx, Rowsz, ETx, ETz, CT){
    //KeyStone Jack Hole Dimensions
    KHAx = 15; KHAz = 19.7;
    //Keystone Faceplate - Entire Piece which keystone holes will be removed from
    Kx = (Colsx * KHAx) + (2 * ETx) + ((Colsx-1)*CT); 
    Ky = 1.5; 
    Kz = (Rowsz * KHAz) + (2 * ETz) + ((Rowsz-1)*CT);
    color("Aqua", 1.0){
    difference(){
    cuboid([Kx,Ky,Kz], rounding=0.5, p1=[0,0,0]);
    for (Movz=[0:1:Rowsz-1]){
        for (Movx=[0:1:Colsx-1]) {
           #cuboid([KHAx,Ky+2,KHAz],p1=[ETx+(Movx*(KHAx+CT)),-1,ETz+(Movz*(KHAz+CT))]); 
        }
    }
    //translate([oset(Kx, KHAx),-1,oset(Kz, KHAz)]) #cuboid([KHAx,Ky+2,KHAz],center=BaseCntr);
    }
    }
}



KeystonePanel(5,2,10,5,5);