// inlet into reductor hole
// with anti-slip notch

od = 17.6;

od2 = 27; // spacer touch reductor hole
h2  = 10; // height spacer

od3 = 50; // counter ring with screw holes for counting
h3  =  8; // ring height

notch_thick = 2;
notch_width = 5;

id = 9;
h  = 30; // total height
// cylindrical spacer to choose
// correct angle of the bearings

screws_n = 8; // number of screw holes
screws_d = 3; // screw hole

screws_h = 15; // screw hole depth

module notch()
{
  translate([od/2,0,h/2])
    cube([notch_thick*2, notch_width,h],center=true);
}

module bulk()
{
  cylinder(d=od,  h=h,     $fn=64);
  cylinder(d=od2, h=h2+h3, $fn=64);
  cylinder(d=od3, h=h3,    $fn=screws_n);
  notch();
}

module m8hole()
{
  translate([0,0,-0.001])
    cylinder(d=id, h=h+1, $fn=32);
}

module screwholes()
{
  for(i = [0:screws_n-1])
    rotate([0,0,360/screws_n*(i+0.5)])
      translate([0,0,h3/2])
        rotate([90,0,0])
          translate([0,0,od3/2-screws_h])
          cylinder(d=screws_d,h=od3,$fn=12);
}

// drills holes in the bulk
module inlet()
{
   difference()
   {
     bulk();
     m8hole();
     screwholes();
   }
}

inlet();
