import cadquery as cq
from cadquery.vis import show


def creation(KeystoneNumX,KeystoneNumY,OuterEdgeX,OuterEdgeY,InternalEdge):
    KeystoneJackHoleX=15
    KeystoneJackHoleY=19.7
    KeystoneBoxZ=1.5
    KeystoneBoxX = (KeystoneNumX * KeystoneJackHoleX) + (2 * OuterEdgeX) + ((KeystoneNumX-1)*InternalEdge) 
    KeystoneBoxY = (KeystoneNumY * KeystoneJackHoleY) + (2 * OuterEdgeY) + ((KeystoneNumY-1)*InternalEdge)
    #Keystone Faceplate - Entire Piece which keystone holes will be removed from
    KeystoneFaceplate = cq.Workplane("XY").center(KeystoneJackHoleX,KeystoneJackHoleY).box(KeystoneBoxX, KeystoneBoxY, KeystoneBoxZ)
    #for (){

    #}
    KeystonePanelRemovedSlots = KeystoneFaceplate#.faces(">Z").circle(0.25)#.extrude()#.box(KeystoneJackHoleX,KeystoneJackHoleY).extrude(1)
    KeystonePanelFinal = KeystonePanelRemovedSlots
    return KeystonePanelFinal

#     for (Movz=[0:1:Rowsz-1]){
#         for (Movx=[0:1:Colsx-1]) {
#            #cuboid([KHAx,Ky+2,KHAz],p1=[ETx+(Movx*(KHAx+CT)),-1,ETz+(Movz*(KHAz+CT))]); 
#         }
#     }

#def show(*objs: Showable,scale: float = 0.2,alpha: float = 1,tolerance: float = 1e-3,edges: bool = False,specular: bool = True,title: str = "CQ viewer",**kwrags: Any,):
result = creation(5,2,10,5,5)
show(result)