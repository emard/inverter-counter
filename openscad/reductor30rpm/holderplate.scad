// reductor raster 52x80.5
// 80.5x75.5, rupe d=8 mm

// holder za inverter, senzor i buttone

// inverter rupe 118x56 3 rupe
// inverter kutija base 67x129 d=5 mm
// od gornje strane do senzora 32 mm, od sredine (80.5
// od sredine do senzora 48 mm

sensor_pos = [-48,80.5/2-32];
thick = 4;
move_up = 20;

btn_screw_dia  = 16; 
btn_outer_dia  = 19;
btn_holder_dia = 29;
btn_pos = [[-37/2,72],[37/2,72]];

module btn_holes()
{
  for(xy = btn_pos)
    translate(xy)
      cylinder(d=btn_screw_dia,h=thick+1,$fn=32,center=true);
}

module btn_holders()
{
  for(xy = btn_pos)
    translate(xy)
      cylinder(d=btn_holder_dia,h=thick,$fn=32,center=true);

  // straignth extension bottom
  bot_ext = 20;
  for(xy = btn_pos)
    translate(xy+[0,-bot_ext/2])
      cube([btn_holder_dia,bot_ext,thick],center=true);

  // bar between btns
  if(1)
  translate([0,btn_pos[0][1]])
  // cube([10,10,10],center=true);
  cube([-btn_pos[0][0]+btn_pos[1][0],btn_holder_dia,thick],center=true);

}

module sensor_hole()
{
  translate(sensor_pos)
    cylinder(d=13,h=thick+1,$fn=32,center=true);
}

module sensor_holder()
{
  translate(sensor_pos)
    cylinder(d=25,h=thick,$fn=32,center=true);
}

module inverter_holes()
{
  inverter_hole_list=[[-56/2,-118/2],[56/2,-118/2],[0,118/2]];
  for(xy = inverter_hole_list)
   translate(xy)
     cylinder(d=3,h=thick+1,$fn=32,center=true);
}

module reductor_holes()
{
  reductor_hole_raster = [80.5,75.5];
  for(i=[-1,1])
    for(j=[-1,1])
      translate([reductor_hole_raster[0]*i/2,reductor_hole_raster[1]*j/2])
        cylinder(d=5,h=thick+1,$fn=32,center=true);
}

module cut_center()
{
    base = [64,100,thick+1];
    rounding = 8;
    minkowski()
    {
      cube(base-[rounding*2,rounding*2,base[2]/2],center=true);
      cylinder(r=rounding,h=base[2]/2,center=true);
    }
}

module inverter_base()
{
  base = [99,129,thick];
  rounding = 10;
  difference()
  {
    union()
    {
      minkowski()
      {
        cube(base-[rounding*2,rounding*2,base[2]/2],center=true);
        cylinder(r=rounding,h=base[2]/2,center=true);
      }
      translate([0,-move_up,0])
        sensor_holder();
      btn_holders();
    }
    inverter_holes();
    translate([0,-move_up,0])
    {
      reductor_holes();
      sensor_hole();
    }
    cut_center();
    btn_holes();
  }
}


// projection()
inverter_base();
