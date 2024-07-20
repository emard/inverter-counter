od = 17;

//notch_thick = 2;
//notch_width = 4.5;

id = 9;
h  = 39;
// cylindrical spacer to choose
// correct angle of the bearings
module spacer()
{
   difference()
   {
     cylinder(d=od, h=h, $fn=32, center=true);
     cylinder(d=id, h=h+1, $fn=32, center=true);
   }
}

spacer();
